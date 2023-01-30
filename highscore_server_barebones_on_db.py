import sqlite3

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_url_path="/", static_folder="www")
# MarkO: This is required for clients running on different protocol/DNS/port numbers.
# I have a presentation on CORS if you need to know more.
CORS(app)


class HighScores:
    def __init__(self, database_file_name):
        self.database_file_name = database_file_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.database_file_name)
        cur = conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS highscores " \
              "(id PRIMARY KEY, name TEXT NOT NULL, score INTEGER NOT NULL, game TEXT NOT NULL)"
        cur.execute(sql)
        conn.commit()

    def get(self, game):
        conn = sqlite3.connect(self.database_file_name)
        # MarkO: This "row_factory" has SQLite results include the column name.
        # Without this line you would need to use number based indexing to retrieve
        # results.
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "SELECT * FROM highscores where game = ? " \
              "ORDER BY score DESC LIMIT 10"
        result = cur.execute(sql, [game])
        scores = []
        for score in result:
            scores.append({"name": score["name"], "score": score["score"]})
        return scores

    def insert_score(self, name, score, game):
        conn = sqlite3.connect(self.database_file_name)
        cur = conn.cursor()
        sql = "INSERT INTO highscores VALUES (?, ?, ?)"
        cur.execute(sql, [name, score, game])
        conn.commit()


@app.route("/highscores/<game>", methods=["GET", "POST"])
def handle_highscores(game):
    if request.method == "POST":
        body = request.json
        try:
            highscores.insert_score(body["name"], body["score"], game)
            result = "ok"
            error = ""
        except HighScores as e:
            result = "error"
            error = f"Missing required field ({e})"
        except Exception as e:
            result = "error"
            error = str(e)
        return jsonify({"result": result, "error": error})
    elif request.method == "GET":
        scores = highscores.get(game)
        scores_dict = {"scores": scores}
        return jsonify(scores_dict)


@app.route("/")
@app.route("/jquery")
def hello_jquery():
    return send_from_directory("www", "highscore_jquery.html")


@app.route("/javascript")
def hello_javascript():
    return send_from_directory("www", "highscore_js.html")


highscores = HighScores("scores.db")
app.run(debug=True, host="127.0.0.1", port=5001)