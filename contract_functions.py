import os
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

def mint(receiverAddress, bsc_endpoint):

    w3 = Web3(Web3.HTTPProvider(bsc_endpoint))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    logger.debug(f"Web3 connected to bsc at {bsc_endpoint}: {w3.isConnected()}")

    with open("./Abi_contract.json") as f:
        info_json = json.load(f)
    abi = info_json
    print(os.getenv("CONTRACT_ADDRESS"))
    CPContract = w3.eth.contract(address=os.getenv("CONTRACT_ADDRESS"), abi=abi)

    txn = CPContract.functions.mint(receiverAddress)
    nonce = w3.eth.get_transaction_count(os.getenv("CONTRACT_OWNER_ADDRESS"))

    options = txn.buildTransaction({
        "chainId": 97,
        # 'to': '0xc05D4536846168b93a83F289d8E14283D43cd515',
        'gas': txn.estimateGas({"from": os.getenv("CONTRACT_OWNER_ADDRESS")}),
        'gasPrice': w3.toWei(10, "gwei"),
        'nonce': nonce

    })

    logger.info(f"Built transaction with next options: {options}")
    signedTxn = w3.eth.account.sign_transaction(options, private_key=os.getenv("PRIVATE_KEY"))
    logger.info(f"Signed contract: {signedTxn}")
    w3.eth.send_raw_transaction(signedTxn.rawTransaction)

    txnHash = w3.toHex(w3.keccak(signedTxn.rawTransaction))

    txnReceipt = w3.eth.wait_for_transaction_receipt(txnHash)
    logs = CPContract.events.Transfer().processReceipt(txnReceipt)
    tokenId = int(logs[0]['args']['tokenId'])

    return tokenId




