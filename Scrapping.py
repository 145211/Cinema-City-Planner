import json
from datetime import date, timedelta

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import Addresses
import MatplotCCG


def scrape(addresses, showtimes, dates):
    session = HTMLSession()
    for date in dates:
        for cinema in addresses.keys():
            specific_element = []
            changed = False
            while not specific_element:
                response = session.get(addresses[cinema] + "?at={}".format(date))
                response.raise_for_status()
                response.html.render()
                tag = "qb-movie-details"
                soup = BeautifulSoup(response.html.html, "html.parser")
                specific_element = soup.find_all(class_=tag)
                changed = True

            #todo check if empty days correct
            if changed:
                showtimes[cinema][str(date)] = specific_element

    return showtimes


def enlist(screenings, cinema):
    cinemaDays = {}

    for day in screenings[cinema]:
        moviesDay = []
        movie_num = 0
        for item in screenings[cinema][day]:
            tmp_screenings = []

            title = item.find("h3", {"class": "qb-movie-name"}).text
            # print(title)

            details = item.find("div", {"class": "qb-movie-info"}).find_all("span")
            genre = details[0].text[0:-2]
            duration = int(details[1].text.split(" ")[0])
            # print(genre, duration)

            screens = item.find_all("div", {"class": "qb-movie-info-column"})
            isnt_played = False

            # for all screening types get their type, language and hours
            for screening in screens:
                # if a movie is not played that day ignore it
                if movie_type := screening.find("ul", {"class": "qb-screening-attributes"}):
                    movie_type = movie_type.text

                else:
                    isnt_played = True
                    continue

                movie_lang = screening.find("ul", {"class": "qb-movie-attributes"}).text.replace(" · ", " ")
                # print(movie_lang)

                hours_temp = screening.find_all("a")
                # print(hours_temp)

                # for each screening calculate what time it ends
                start_hours = []
                end_hours = []
                for hour in hours_temp:
                    tmp_hour = hour.text.replace(" ", "")
                    start_hours.append(tmp_hour)
                    end_hours.append(MatplotCCG.add_mins(tmp_hour, duration))

                tmp_screenings.append(
                    {"type": movie_type, "language": movie_lang, "start": start_hours, "end": end_hours})

                tmp_movie = {"title": title, "duration": duration, "screenings": tmp_screenings}
                # print(tmp_movie)

            if isnt_played:
                continue

            moviesDay.append(tmp_movie)

            movie_num += 1

        cinemaDays[day] = moviesDay

    # Save dictionary to a JSON file
    with open('screenings/{}.json'.format(cinema), 'w') as json_file:
        json.dump(cinemaDays, json_file, indent=4)

    return cinemaDays


if __name__ == "__main__":
    addresses = Addresses.addresses

    dates = []
    showtimes = {key: {} for key in addresses}

    for days in range(21):
        day = date.today() + timedelta(days=days)
        dates.append(day)

    showtimes = scrape(addresses, showtimes, dates)

    for x in addresses.keys():
        test = enlist(showtimes, x)
