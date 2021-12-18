import sqlite3
import json


def run_query(sql_query, parametrs=(), is_json=True):
    con = sqlite3.connect("netflix.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if len(parametrs) > 0:
        results = cur.execute(sql_query, parametrs)
    else:
        results = cur.execute(sql_query)
    if is_json:
        return json.dumps([dict(result) for result in results.fetchall()])
    else:
        return results


def get_like_from(word):
    return f"%{word}%"


def get_top10_by_genre(genre):
    genre = get_like_from(genre)
    sqlite_query = """select title, description from netflix where listed_in like ? order by release_year desc limit 10"""
    return run_query(sqlite_query, (genre,))


def get_coactors(actor1, actor2):
    sqlite_query = """select `cast` from netflix where `cast` like ? and `cast` like ?"""
    results = run_query(sqlite_query, (get_like_from(actor1), get_like_from(actor2),), False)
    coactors = set()
    for result in results.fetchall():
        print(result)
        result = dict(result)
        for actor in result["cast"].split(", "):
            if actor != actor1 and actor != actor2:
                coactors.add(actor)
    return coactors


def find_by_type_year_genre(type, year, genre):
    sqlie_query = """select title, description from netflix where `type`=? and release_year=? and listed_in like ?"""
    return run_query(sqlie_query, (type, year, get_like_from(genre)))


print(get_top10_by_genre("Documentaries"))
print(get_coactors("Rose McIver", "Ben Lamb"))
print(find_by_type_year_genre("Movie", 2019, "Documentaries"))
