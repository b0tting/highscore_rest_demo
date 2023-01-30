from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path="/", static_folder="www")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
db = SQLAlchemy(app)
CORS(app)


def result_to_dict(sql_result):
    result_dict = []
    for row in sql_result:
        result_dict.append(({column.name: str(getattr(row, column.name)) for column in row.__table__.columns}))
    return result_dict


class Highscores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    score = db.Column(db.String(80), nullable=False)
    game = db.Column(db.String(120), nullable=False)


@app.route("/highscores/<game>", methods=["GET", "POST"])
def handle_highscores(game):
    if request.method == "POST":
        body = request.json
        try:
            score = Highscores(name=body["name"], score=body["score"], game=game)
            db.session.add(score)
            db.session.commit()
            result = "ok"
            error = ""
        except Exception as e:
            result = "error"
            error = str(e)
        return jsonify({"result": result, "error": error})
    elif request.method == "GET":
        scores = Highscores.query.filter_by(game=game)
        scores_dict = {"scores": result_to_dict(scores)}
        return jsonify(scores_dict)


@app.route("/")
@app.route("/jquery")
def hello_jquery():
    return send_from_directory("www", "highscore_jquery.html")


@app.route("/javascript")
def hello_javascript():
    return send_from_directory("www", "highscore_js.html")

# Note that we need to push the create_all below the Highscores class
# definition, otherwise if it's a new database SQLALchemy will not
# create the highscores table
db.create_all()
app.run(debug=True, host="127.0.0.1", port=5001)
