import os
import datetime
from flask import jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect
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
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

logger.debug(f"Started app successfully with next config: {app.config}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import CrestoPass

logger.debug("Connected to db successfully")

BSC_MAINNET = "https://bsc-dataseed1.binance.org"
BSC_MAINNET_CHAIN_ID = int(56)
BSC_TESTNET = "https://data-seed-prebsc-1-s1.binance.org:8545"
BSC_TESTNET_CHAIN_ID = int(97)

gen_dict = {
    "cresto_pass": {
        "name": "CRESTO PASS",
        "category": "cresto_pass",
        "image": "ipfs://QmcZW6yPYtyLMRPtQzWEzWnXg1VRaMBA784wjyg7GPo3WE",
        "description": (
            "Cresto Pass is a game pass that gives the following bonuses:\n\n"+
            "1. Gives you the opportunity to buy 5 chests at cresto.app at a 30% discount after launching the game.\n\n"+
            "2. Gives you a greatly increased chance (75%) of participating in IDO at cresto.app\n\n"+
            "3. Gives access to private restaurant auctions.\n\n"+
            "4. Allows you to get 1 vote in DAO Cresto\n\n"+
            "The only way to get a Cresto Pass is to win it in an airdrop."
        )
    },
    "cresto_voucher": {
        "name": "CRESTO VOUCHER",
        "category": "cresto_voucher",
        "image": "ipfs://Qmdqkp2c4ivyqcLJ5sFcTUGDMUpAuF1V56oMqhiouaRkb4",
        "description": "Gives 30% off a single purchase at cresto.app"
    }
}

@app.route("/api/", methods=["GET", "POST"])
def index():
    errors = []
    if request.method == "POST":
        tokenId = request.form["tokenId"]
        try:
            tokenId = int(tokenId)
            return redirect(f"/api/cresto-nfts/{tokenId}/")
        except Exception as e:
            print(e)
            error = "Wrong format! Enter integer tokenId i.e. 0"
            return redirect(url_for(".fail_index", error=error))

    try:
        errors.append(request.args["error"])
    except KeyError:
        pass

    return render_template("index.html", errors=errors)

@app.route("/api/", methods=["GET"])
def fail_index():
    pass


@app.route("/api/cresto-nfts/mint/", methods=["GET", "POST"])
def add_token():
    errors = []
    text = None
    if request.method == "POST":

        owner_id = request.form["owner_id"]
        nft_selected = request.form["cresto_nft"]
        print(owner_id)
        password = request.form["password"]
        if password == os.getenv("MINT_PASSWORD"):

            try:
                if app.config["DEBUG"] == True:
                    token_id = mint(owner_id, BSC_TESTNET, BSC_TESTNET_CHAIN_ID)
                else:
                    token_id = mint(owner_id, BSC_MAINNET, BSC_MAINNET_CHAIN_ID)
                logger.info(f"Minting token with tokenId {token_id}...")
                token = CrestoPass(
                    id=token_id,
                    name=gen_dict[nft_selected]["name"],
                    category=gen_dict[nft_selected]["category"],
                    image=gen_dict[nft_selected]["image"],
                    owner_id=owner_id,
                    description=gen_dict[nft_selected]["description"],
                    mintedAt=datetime.datetime.now()
                )
                db.session.add(token)
                db.session.commit()
                return redirect(url_for(".success_mint", tokenId=token_id))
            except Exception as e:
                error = f"Unable to add item to DB. Reason: {e}"
                logger.error(f"Errors happened: {errors}")
                return redirect(url_for(".fail_mint", error=error))
        else:
            error = "Wrong password!"
            logger.error(f"Errors happened: {errors}")
            return redirect(url_for(".fail_mint", error=error))
    
    try:
        tokenId = request.args["tokenId"]
        text = f"Created new token with tokenId: {tokenId}"
    except KeyError:
        pass

    try:
        errors.append(request.args["error"])
    except KeyError:
        pass

    return render_template("mint_page.html", errors=errors, text=text)

@app.route("/api/cresto-nfts/mint/", methods=["GET"])
def success_mint():
    pass

@app.route("/api/cresto-nfts/mint/", methods=["GET"])
def fail_mint():
    pass


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
        return jsonify(token.as_dict())
    except AttributeError:
        return render_template("one_token_error_page.html")

