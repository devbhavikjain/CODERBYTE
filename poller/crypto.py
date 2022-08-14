import requests
import os
# Logging
import logging
logging.basicConfig(format='%(asctime)s -  %(levelname)s - %(message)s')
logger = logging.getLogger('crypt')
logger.setLevel(logging.INFO)


def get_current_coin_data(coinid):
    """
    Fetches specific coin data from CoinGecko API
    Args:
        coin_id (str) : Unique ID of the coin in CoinGecko
    Returns:
        dict: all data received from the API for the coinid
    """
    logger.info(f"Fetching Price from CoinGecko for coinid: {coinid}..")

    # Load config
    host_scheme = os.getenv("CRYPTO_ENDPOINT_SCHEME")
    host_name = os.getenv("CRYPTO_ENDPOINT_HOST")
    host_path = os.getenv("CRYPT_ENDPOINT_PATH")

    request_params = {
        "tickers" : False,
        "community_data" : False,
        "developer_data" : False,
        "sparkline" : False
    }

    full_url = "https://api.coingecko.com/api/v3/coins/" + coinid
    logger.info(f"Calling {full_url}..")

    response = requests.get(url=full_url, params=request_params)

    return response.json()

def get_coin_price(json_response, currency="usd"):
    """
    Parses API Response to fetch the current price of the coin
    Args:
        json_responsne (dict) : API Response for coin
        current (str) : Currency for which current price is required
    Returns:
        int: Current Price of the coin if found else None
    """
    logger.info("Parsing Response..")
    current_prices = json_response.get(
        "market_data", {}).get("current_price", {})
    if not current_prices:
        logging.error("Current Prices Unavailable!")
        return None

    if currency not in current_prices:
        logging.error(f"Currency {currency} is unavailable in the market!")
        return None

    current_price = current_prices.get(currency)

    return current_price
