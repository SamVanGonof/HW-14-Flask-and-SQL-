from flask import Flask, jsonify, render_template

from utils import *


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True
app.config["JSON_SORT_KEYS"] = False # что бы выводил данные как требуется в условии ДЗ.

"""Решил добавить вьюшку на главную страницу для удобства"""


@app.route('/')
def main_page():
    return render_template("main_page.html")


@app.route('/movie/<title>/')
def get_by_title(title):
    return movie_by_title(title)


@app.route('/movie/<int:year_1>/to/<int:year_2>/')
def get_by_years(year_1, year_2):
    return jsonify(movie_by_years(year_1, year_2))


@app.route('/rating/<category>/')
def get_by_rating(category):
    return jsonify(movie_by_rating(category.lower()))


@app.route('/genre/<genre>/')
def get_by_genre(genre):
    return jsonify(movie_by_genre(genre))


if __name__ == '__main__':
    app.run(port=1212)



