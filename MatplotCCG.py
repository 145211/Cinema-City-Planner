import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import plotly.graph_objects as go


def make_plot(movies, chosen=None):
    titles = []
    xs = []
    ys = []
    scr_cnt = 0

    if chosen is None:
        for movie in movies:
            for screen in movie["screenings"]:
                titles.append("{} {} {}".format(movie["title"], screen["type"], screen["language"]))
                xs.append(list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["start"])))
                ys.append(list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["end"])))
    else:
        print(chosen)
        scr_cnt = 0
        for n in chosen:
            for screen in movies[n]["screenings"]:
                titles.append("{} {} {}".format(movies[n]["title"], screen["type"], screen["language"]))
                xs.append(list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["start"])))
                ys.append(list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["end"])))
                scr_cnt += 1

    with plt.rc_context({'ytick.color': '#d57031',
                         'xtick.color': '#d57031',
                         'axes.facecolor': '#373737',
                         'figure.facecolor': '#1f1f1f'}):
        fig = plt.figure(figsize=(18, 8), dpi=100)
        ax = plt.axes()

    plt.subplots_adjust(left=0.20, right=0.99, top=0.99, bottom=0.05)

    for n in range(len(xs)):
        for i in range(len(xs[n])):
            x1, x2 = xs[n][i], ys[n][i]
            y1, y2 = n, n
            plt.plot([x1, x2], [y1, y2], '-', color='#d57031')

    for n in range(len(xs)):
        for i in range(len(xs[n])):
            x1, x2 = xs[n][i], ys[n][i]
            y1, y2 = n, n
            plt.plot([x1], [y1], '-|', color='#6ccff6')
            plt.plot([x2], [y2], '-x', color='#6ccff6')

    plt.xticks(range(10, 25))
    plt.yticks(range(len(xs)), titles, wrap=True, fontsize=8)
    plt.grid(color='#1f1f1f')

    if chosen is not None:
        if 1 < scr_cnt < 10:
            ax.set_ylim(-1, scr_cnt)

    return fig


def make_plot_plotly(movies, chosen=None):
    titles = []
    all_titles = []
    start_times = []
    end_times = []
    normalized_start_times = []
    normalized_end_times = []

    if chosen is None:
        for movie in movies:
            for screen in movie["screenings"]:
                titles.append("{} {} {}".format(movie["title"], screen["type"], screen["language"]))
                start_times.append(screen["start"])
                end_times.append(screen["end"])
                normalized_start_times.append(list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["start"])))
                normalized_end_times.append(list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["end"])))
                all_titles = titles
    else:
        chosen_decoded = decodeHexChecklist(chosen)
        cnt = 0
        for movie in movies:
            for screen in movie["screenings"]:
                if cnt in chosen_decoded:
                    titles.append("{} {} {}".format(movie["title"], screen["type"], screen["language"]))
                    start_times.append(screen["start"])
                    end_times.append(screen["end"])
                    normalized_start_times.append(
                        list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["start"])))
                    normalized_end_times.append(
                        list(map(lambda x: float(norm_hours(x.replace(":", "."))), screen["end"])))
                all_titles.append("{} {} {}".format(movie["title"], screen["type"], screen["language"]))
                cnt += 1

    fig = go.Figure()
    fig.update_layout(yaxis=dict(autorange="reversed"))

    for n in range(len(normalized_start_times)):
        for i in range(len(normalized_start_times[n])):
            x1, x2 = normalized_start_times[n][i], normalized_end_times[n][i]
            y1, y2 = n, n
            fig.add_trace(go.Scatter(x=[x1, x2], y=[y1, y2], mode='lines', line=dict(color='#d57031'),
                                     hovertemplate="<extra></extra>"))
            fig.add_trace(go.Scatter(x=[x1], y=[y1], mode='markers',
                                     marker=dict(symbol='line-ns', color='#ffffff', line=dict(color='#ffffff', width=5),
                                                 size=10), hovertemplate=f"Start: {start_times[n][i]}<extra></extra>"))
            fig.add_trace(go.Scatter(x=[x2], y=[y2], mode='markers', marker=dict(symbol='x', size=10, color='#ffffff'),
                                     hovertemplate=f"End: {end_times[n][i]}<extra></extra>"))

    fig.update_layout(
        xaxis=dict(tickvals=list(range(10, 25)), gridcolor='#1f1f1f', tickfont=dict(size=12, color='#d57031'),
                   zeroline=False))
    fig.update_layout(yaxis=dict(tickvals=list(range(len(normalized_start_times))), tickmode='array', ticktext=titles,
                                 tickfont=dict(size=12, color='#d57031'),
                                 range=[-0.5, len(normalized_start_times) - 0.5], gridcolor='#808080', zeroline=False))
    fig.update_layout(plot_bgcolor='#373737', yaxis=dict(gridcolor='#1f1f1f'))
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.update_layout(paper_bgcolor='#1f1f1f')
    fig.update_layout(showlegend=False)

    return fig, all_titles


# simple time addition
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

    if t_mins >= 10:
        return "{}:{}".format(t_hour, t_mins)
    else:
        return "{}:0{}".format(t_hour, t_mins)


def norm_hours(hour):
    hour2 = hour.split(".")

    hour2[1] = int(round(np.interp([int(hour2[1])], [0, 60], [0, 100])[0]))

    if 0 < hour2[1] < 10:
        hour2[1] = "0" + str(hour2[1])
    else:
        hour2[1] = str(hour2[1])

    hour2 = ".".join(hour2)

    return hour2


def decodeHexChecklist(hex_code):
    decimal_value = int(hex_code, 16)
    binary_string = bin(decimal_value)[2:].zfill(len(hex_code) * 4)
    reversed_binary_string = binary_string[::-1]
    selected_items = [index for index, bit in enumerate(reversed_binary_string) if bit == '1']

    return selected_items
