import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Result

@app.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"Hello World! x33 secret key : {secret_key}"

@app.route("/<name>")
def hello_name(name):
    return f"Hello {name}"

