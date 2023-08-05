from datetime import date, timedelta
import requests
import json


def scrapping():
    cinemas = json.load(open("cinemas.json", encoding='utf-8'))

    testing = ['kinepolis', 'korona', 'mokotow', 'poznanplaza', 'wroclavia']

    dates = []

    for days in range(21):
        day = date.today() + timedelta(days=days)
        dates.append(day)

    cinema_showings = {key: {} for key in cinemas}

    for cinema in cinema_showings:
        for day in dates:
            cinema_showings[cinema][str(day)] = fetch(cinemas[cinema]['id'], day)

        with open(f'screenings/{cinema}.json', 'w', encoding='utf-8') as json_file:
            json.dump(cinema_showings[cinema], json_file, indent=4, ensure_ascii=False)


def fetch(cinema_id, day):
    url = f'https://www.cinema-city.pl/pl/data-api-service/v1/quickbook/10103/film-events/in-cinema/{cinema_id}/at-date/{day}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "https://www.example.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()['body']

        data = clear_json(data)

        return data
    else:
        return None


def clear_json(data):
    films = {}

    for film in data['films']:
        films[film['id']] = {'title': film['name'],
                             'duration': film['length'],
                             'screenings': []
                             }

    for event in data['events']:
        mov_format, mov_lang = attributer(event['attributeIds'])
        films[event['filmId']]['screenings'].append({'start': event['eventDateTime'][11:16],
                                                     'end': add_mins(event['eventDateTime'][11:16],
                                                                     films[event['filmId']]['duration']),
                                                     'roomBig': event['auditorium'],
                                                     'room': event['auditoriumTinyName'].split()[0],
                                                     'format': mov_format,
                                                     'lang': mov_lang,
                                                     'langForm': mov_format + mov_lang
                                                     })

    return reformatter(films)


def attributer(attrs):
    mov_format = ''

    if 'imax' in attrs: mov_format += 'IMAX '
    if 'vip' in attrs: mov_format += 'VIP '
    if '4dx' in attrs:
        mov_format += '4DX'
    elif '2d' in attrs:
        mov_format += '2D'
    elif '3d' in attrs:
        mov_format += '3D'
    if 'dolby-atmos' in attrs: mov_format += ' Dolby Atmos'
    if 'hfr' in attrs: mov_format += ' HFR'

    mov_lang = ''

    if 'original-lang-pl' in attrs:
        mov_lang += '(BEZ NAPISÓW)'
    elif 'dubbed' in attrs:
        mov_lang += '(DUB '
        mov_lang += next((item for item in attrs if item.startswith('dubbed-')), 'PL').split('-')[-1].upper() + ')'
    elif 'subbed' in attrs:
        mov_lang += next((item for item in attrs if item.startswith('original-')), None).split('-')[2].upper()
        mov_lang += ' (NAP '
        mov_lang += next((item for item in attrs if item.startswith('first-')), None).split('-')[3].upper() + ')'

    return mov_format, mov_lang


def reformatter(films):
    reformatted_films = []
    for data in films.values():
        reformatted_data = {
            "title": data["title"],
            "duration": data["duration"],
            "screenings": []
        }

        screenings_grouped = {}
        for screening in data["screenings"]:
            key = screening["format"] + screening["lang"]
            if key not in screenings_grouped:
                screenings_grouped[key] = {
                    "type": screening["format"],
                    "language": screening["lang"],
                    "start": [],
                    "end": []
                }
            screenings_grouped[key]["start"].append(screening["start"])
            screenings_grouped[key]["end"].append(screening["end"])

        # Convert the grouped screenings to a list
        reformatted_data["screenings"] = list(screenings_grouped.values())
        reformatted_films.append(reformatted_data)

    return reformatted_films


def add_mins(hour, duration):
    t_hour, t_mins = hour.split(":")
    t_hour = int(t_hour)
    t_mins = int(t_mins)

    hours = duration // 60
    mins = duration % 60

    if t_mins + mins >= 60:
        t_hour += 1
        t_mins = t_mins + mins - 60
    else:
        t_mins += mins

    t_hour += hours

    return f"{t_hour:02d}:{t_mins:02d}"


if __name__ == "__main__":
    scrapping()
