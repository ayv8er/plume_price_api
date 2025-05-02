import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from web3 import Web3

load_dotenv()

app = FastAPI()

w3_plume = Web3(Web3.HTTPProvider("https://rpc.plume.org"))

POOL_LENS_ADDRESS = "0xBf0D89E67351f68a0a921943332c5bE0f7a0FF8A"
PLUME_PUSD_POOL = "0x4A14398C5c5B4B7913954cB82521fB7afA676314"

POOL_LENS_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "pool", "type": "address"}],
        "name": "getPoolPrice",
        "outputs": [{"internalType": "uint256", "name": "price", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

alchemy_rpc = os.getenv("ALCHEMY_RPC")
w3_mainnet = Web3(Web3.HTTPProvider(alchemy_rpc))

CHAINLINK_ETH_USD = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"

CHAINLINK_ABI = [
    {
        "name": "latestRoundData",
        "outputs": [
            {"type": "uint80"}, {"type": "int256"}, {"type": "uint256"},
            {"type": "uint256"}, {"type": "uint80"}
        ],
        "inputs": [],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "name": "decimals",
        "outputs": [{"type": "uint8"}],
        "inputs": [],
        "stateMutability": "view",
        "type": "function"
    }
]

@app.get("/price")
def get_price(denom: str = Query(default="usd", enum=["usd", "eth"])):
    try:
        lens = w3_plume.eth.contract(address=POOL_LENS_ADDRESS, abi=POOL_LENS_ABI)
        raw_plume_pusd = lens.functions.getPoolPrice(PLUME_PUSD_POOL).call()
        plume_pusd = raw_plume_pusd / 1e18

        price = plume_pusd

        if denom == "eth":
            chainlink = w3_mainnet.eth.contract(address=CHAINLINK_ETH_USD, abi=CHAINLINK_ABI)
            raw_answer = chainlink.functions.latestRoundData().call()[1]
            decimals = chainlink.functions.decimals().call()
            eth_usd = raw_answer / (10 ** decimals)

            price = plume_pusd / eth_usd

        return {
            "symbol": "PLUME",
            f"price_{denom}": str(price),
        }

    except Exception as e:
        return {"error": str(e)}