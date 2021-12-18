import sqlite3
import json
from flask import Flask, jsonify
from functions import *

app = Flask(__name__, static_folder="css")


#
#
@app.route('/movie/title/<string:title>')
def title(title):
    sqlite_query = ("""select title, country, MAX(release_year) as release_year, listed_in as genre, description 
                        from netflix
                        where title=?""")
    return jsonify(run_query(sqlite_query, (title,)))


@app.route('/movie/year/<int:year>')
def year(year):
    sqlite_query = ("""select title, release_year
                            from netflix
                            where release_year=? limit 100""")
    return jsonify(run_query(sqlite_query, (year,)))


@app.route('/rating/<string:group>')
def rating(group):
    rating = ["", ""]
    if group == "children":
        rating = ["G", "G"]
    elif group == "family":
        rating = ["PG", "PG-13"]
    elif group == "adult":
        rating = ["R", "NC-17"]
    sqlite_query = ("""select title, rating, description from netflix where rating IN (?,?)""")
    return jsonify(run_query(sqlite_query, (rating[0], rating[1],)))


if __name__ == "__main__":
    app.run(debug=True)
