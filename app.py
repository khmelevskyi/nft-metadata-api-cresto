import os
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request
from flask import Flask
from loguru import logger
from dotenv import load_dotenv

from contract_functions import mint


logger.add(
    "debug.log",
    format="{time} {level} {message}\n",
    level="DEBUG",
    rotation="30 KB",
    compression="zip",
)
load_dotenv()


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
CATEGORY = "cresto_pass"
IMAGE = "ipfs://QmcZW6yPYtyLMRPtQzWEzWnXg1VRaMBA784wjyg7GPo3WE"
DESCRIPTION = str(
    "Cresto Pass is a game pass that gives the following bonuses:\n\n"+
    "1. Gives you the opportunity to buy 5 chests at cresto.app at a 30% discount after launching the game.\n\n"+
    "2. Gives you a greatly increased chance (75%) of participating in IDO at cresto.app\n\n"+
    "3. Gives access to private restaurant auctions.\n\n"+
    "4. Allows you to get 1 vote in DAO Cresto\n\n"+
    "The only way to get a Cresto Pass is to win it in an airdrop."
)


@app.route("/api/", methods=["GET", "POST"])
def index():
    return "CRESTO API"


@app.route("/api/cresto-nfts/mint/", methods=["GET", "POST"])
def add_token():
    errors = []
    if request.method == "POST":
        
        owner_id = request.form["owner_id"]
        print(owner_id)
        password = request.form["password"]
        if password == os.getenv("MINT_PASSWORD"):

            try:
                if app.config["DEBUG"] == True:
                    token_id = mint(owner_id, BSC_TESTNET)
                else:
                    token_id = mint(owner_id, BSC_MAINNET)
                logger.info(f"Minting token with tokenId {token_id}...")
                token = CrestoPass(
                    id=token_id,
                    name=NAME,
                    category=CATEGORY,
                    image=IMAGE,
                    owner_id=owner_id,
                    description=DESCRIPTION
                )
                db.session.add(token)
                db.session.commit()

                text = f"Created new token with tokenId: {token_id}"
                logger.info(text)
                return render_template("index.html", errors=errors, text=text)
            except Exception as e:
                errors.append(f"Unable to add item to DB. Reason: {e}")
                logger.error(f"Errors happened: {errors}")
        else:
            errors.append("Wrong password!")
            logger.error(f"Errors happened: {errors}")
            
    return render_template("index.html", errors=errors)


@app.route("/api/cresto-nfts/", methods=["GET"])
def get_all_tokens():
    tokens = db.session.query(CrestoPass).all()
    tokens_json = [c.as_dict() for c in tokens]
    return jsonify(tokens_json)


@app.route("/api/cresto-nfts/<id>/", methods=["GET"])
def get_one_token(id):
    token = db.session.query(CrestoPass).get(id)
    print(token)
    try:
        return token.as_dict()
    except AttributeError:
        return "Sorry, token doesn't exists :("

