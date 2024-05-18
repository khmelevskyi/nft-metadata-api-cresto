# nft-metadata-api-cresto



## About
This project is an API service which:
- has an endpoint to view your NFT token's metadata
- has an endpoint to view all minted tokens' metadata
- has an endpoint to mint a token (restricted access: for NFT project owners only)

## Getting Started
```
git checkout git@github.com:khmelevskyi/nft-metadata-api-cresto.git
cd nft-metadata-api-cresto
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Credentials
First, copy .env.example into .env
```
cp .env.example .env
```
Second, you need to enter the next data into your .env:
- DEV_DATABASE_URL/DATABASE_URL - the URL to your database
- APP_SETTINGS - can be either "config.DevelopmentConfig", or "config.StagingConfig", or "config.ProductionConfig"
- CONTRACT_OWNER_ADDRESS - the wallet address with which you deployed the Smart Contract for your NFT token
- PRIVATE_KEY_BSCSCAN - the private key which BSCSCAN generated for you when creating API key on your BSCSCAN account
- MINT_PASSWORD - the password to resctrict access to mint functionality of the API service

Third, you will need Abi_contract.json to mint the NFT token. This json file proves that you are the owner of the
deployed token. You can get this Abi_contract.json when you deploy your token. Just copy and paste this file into
Abi_contract/ folder
## Migrate the database
```
flask db upgrade
```

## Start the application
```
python wsgi.py
```
