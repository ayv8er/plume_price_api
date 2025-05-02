# Plume Price API

This FastAPI application provides an endpoint to fetch the current price of PLUME/PUSD from the Plume network.

## Functionality

The `main.py` script uses `web3.py` to interact with smart contracts on both the Plume network and Ethereum mainnet.

1.  It connects to the Plume network RPC (`https://rpc.plume.org`) to query a Pool Lens contract (`0xBf0D89E67351f68a0a921943332c5bE0f7a0FF8A`) for the PLUME/PUSD price from a specific pool (`0x4A14398C5c5B4B7913954cB82521fB7afA676314`).
2.  It connects to the Ethereum mainnet using an Alchemy RPC URL provided via the `ALCHEMY_RPC` environment variable.
3.  It defines a FastAPI endpoint at `/price`.

## Endpoint: `/price`

-   **Method:** GET
-   **Query Parameters:**
    -   `denom` (optional): Specifies the denomination for the price. Accepts `usd` (default) or `eth`.
-   **Functionality:**
    -   Fetches the raw PLUME/PUSD price from the Plume network pool.
    -   Formats the price (divides by 1e18).
    -   If `denom` is `eth`, it fetches the current ETH/USD price from the Chainlink oracle (`0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419`) on Ethereum mainnet and calculates the PLUME price in ETH (PLUME/PUSD divided by ETH/USD).
    -   If `denom` is `usd` or not provided, it returns the PLUME/PUSD price.

## Response Format

The endpoint returns a JSON object:

```json
{
  "symbol": "PLUME",
  "price_usd": "<price_in_usd>" 
}
```

Or, if `denom=eth` is specified:

```json
{
  "symbol": "PLUME",
  "price_eth": "<price_in_eth>"
}
```

In case of an error during processing, it returns:

```json
{
  "error": "<error_message>"
}
```

## Setup

1.  Install dependencies: `pip install -r requirements.txt` (You might need to create this file).
2.  Create a `.env` file in the root directory.
3.  Add your Alchemy RPC URL to the `.env` file:
    ```
    ALCHEMY_RPC=https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY
    ```
4.  Run the FastAPI application: `uvicorn main:app --reload`
