import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import plotly.graph_objects as go

from MatplotCCG import norm_hours


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
