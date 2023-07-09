# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, request

from MatplotCCG import make_plot_plotly

static_folder = r"/home/Victorus/mysite/"
static_folder = r"C:/Users/Victorus/PycharmProjects/Fixed2/Personal/CCG2/"

app = Flask(__name__, static_folder=static_folder)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def home():
    return render_template("home.html")


@app.route("/ccg", methods=("GET", "POST"), strict_slashes=False)
def ccg():
    return render_template("grabberSelector.html")


@app.route("/jason", methods=("GET", "POST"), strict_slashes=False)
def jason():
    req_cinema = request.args.get('cinema')
    req_date = request.args.get('date')
    req_chosen = request.args.get('chosen')

    data = json.load(open(f"{static_folder}screenings/{req_cinema}.json", encoding='utf-8'))[req_date]

    fig, titles = make_plot_plotly(data, req_chosen)
    fig.update_layout(height=800)
    div = fig.to_html(full_html=False)

    return render_template("jason.html", data=data, plot_div=div, titles=titles)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
