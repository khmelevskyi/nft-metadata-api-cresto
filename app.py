import os
import Config as config
from flask import Flask

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", config.DevelopmentConfig)
app.config.from_object(env_config)

@app.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"Hello World! x33 secret key : {secret_key}"

