import os
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request
from flask import Flask
from loguru import logger

from contract_functions import mint


logger.add(
    "debug.log",
    format="{time} {level} {message}\n",
    level="DEBUG",
    rotation="30 KB",
    compression="zip",
)


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

logger.debug(f"Started app successfully with next config: {app.config}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import CrestoPass

logger.debug("Connected to db successfully")

BSC_MAINNET = "https://bsc-dataseed1.binance.org"
BSC_TESTNET = "https://data-seed-prebsc-1-s1.binance.org:8545"

NAME = "CRESTO PASS"
SYMBOL = "CRESTOPASS"
IMAGE = "ipfs://QmcZW6yPYtyLMRPtQzWEzWnXg1VRaMBA784wjyg7GPo3WE"
DESCRIPTION = "demo test nft token"


@app.route("/", methods=["GET", "POST"])
def index():
    return "CRESTO API"


@app.route("/cresto_passes/mint/", methods=["GET", "POST"])
def add_token():
    errors = []
    if request.method == "POST":
        
        owner_id = request.form["owner_id"]
        print(owner_id)

        try:
            if app.config["DEBUG"] == True:
                token_id = mint(owner_id, BSC_TESTNET)
            else:
                token_id = mint(owner_id, BSC_MAINNET)
            token = CrestoPass(
                id=token_id,
                name=NAME,
                symbol=SYMBOL,
                image=IMAGE,
                owner_id=owner_id,
                description=DESCRIPTION
            )
            db.session.add(token)
            db.session.commit()
        except:
            logger.error(f"Errors happened: {errors}")
            errors.append("Unable to add item to DB")
            
    return render_template("index.html", errors=errors)


@app.route("/cresto_passes/", methods=["GET"])
def get_all_tokens():
    tokens = db.session.query(CrestoPass).all()
    tokens_json = [c.as_dict() for c in tokens]
    return jsonify(tokens_json)


@app.route("/cresto_passes/<id>/", methods=["GET"])
def get_one_token(id):
    token = db.session.query(CrestoPass).get(id)
    print(token)
    try:
        return token.as_dict()
    except AttributeError:
        return "Sorry, token doesn't exists :("
