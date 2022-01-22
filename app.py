import os
import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request
from flask import Flask

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Result

@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    if request.method == "POST":
        
        title = request.form["title"]
        print(title)

        try:
            result = Result(title=title)
            db.session.add(result)
            db.session.commit()
        except:
            errors.append("Unable to add item to DB")
            
    return render_template("index.html", errors=errors)


@app.route("/mint", methods=["GET", "POST"])
def add_token():
    errors = []
    if request.method == "POST":
        
        title = request.form["title"]
        print(title)

        try:
            result = Result(title=title)
            db.session.add(result)
            db.session.commit()
        except:
            errors.append("Unable to add item to DB")
            
    return render_template("index.html", errors=errors)


@app.route("/tokens")
def get_all_tokens():
    tokens = db.session.query(Result).all()
    tokens_json = [c.as_dict() for c in tokens]
    return jsonify(tokens_json)


@app.route("/tokens/<id>")
def get_one_token(id):
    token = db.session.query(Result).get(id)
    print(token)
    return token.as_dict()

