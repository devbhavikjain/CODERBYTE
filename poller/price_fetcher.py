import os

# Logging
import logging
logging.basicConfig(format='%(asctime)s -  %(levelname)s - %(message)s')
logger = logging.getLogger('prices')
logger.setLevel(logging.INFO)

from db_operations import DB

import crypto
from email_handler import send_email



def load_price_and_insert(coin_id):
    """
    Fetches current price of the coin and Inserts into DB
    Args:
        coin_id (str) : Unique ID of the coin in CoinGecko
    Returns:
        price: integer representing current Price of the Coin
    """
    logger.info(f"Fetching..")

    # Call the API and get response
    results = crypto.get_current_coin_data(coin_id)

    # Parse the API response to get price
    price = crypto.get_coin_price(results)

    # Discard Failed/Invalid responses
    if price is None:
        logger.error("Price fetched is NULL, skipping DB insert..")
        return None

    # Insert Current Price into DB
    insert_coin_price(price)

    return price

def check_and_alert(current_price):
    """
    Triggers Email Alert if current price is less than MIN_PRICE or more than MAX_PRICE
    Args:
        current_price (int): current price of the coin
    Returns:
    """

    send_alert = False
    MIN_PRICE = int(os.getenv('MIN_USD', 24000))
    MAX_PRICE = int(os.getenv('MAX_USD', 25000))

    logger.info(f"Checking Price breach against MIN={MIN_PRICE} AND MAX={MAX_PRICE}..")

    if current_price > MAX_PRICE:
        logger.info(f"Current Price {current_price} breaches MAX_PRICE")
        email_subject = "MAX Price Limit Breach for bitcoin"
        email_body = f"""Please note, price for bitcoin has breached
        the MAX_PRICE set at USD {MAX_PRICE},
        current price is USD {current_price}"""
        send_alert = True
    elif current_price < MIN_PRICE:
        logger.info(f"Current Price {current_price} breaches MIN_PRICE")
        email_subject = "MIN Price Limit Breach for bitcoin"
        email_body = f"""Please note, price for bitcoin has breached
        the MIN_PRICE set at USD {MIN_PRICE},
        current price is USD {current_price}"""
        send_alert = True
    else:
        logger.info("No Price breach!")

    if send_alert:
        # Load config from env
        email_receiver = os.getenv("EMAIL_RECEIVER")
        email_sender = os.getenv("EMAIL_SENDER")

        logger.info("Sending Alert Email...")
        send_email(email_sender, email_receiver, email_subject, email_body)


def insert_coin_price(price):

    insert_query = """INSERT INTO bitcoin(price,utctime) 
    VALUES (?,datetime('now'))"""
    params = [price]
    logger.info(f"Inserting price {price}..")

    db_obj = DB('crypto.db')

    db_obj.insert(insert_query, params)


if __name__ == "__main__":
    import time
    INTERVAL_SECONDS = 30
    start_time = time.time()
    while True:
        # Load Current price
        coin_price = load_price_and_insert('bitcoin')

        # Check and send alert for valid price
        if coin_price is not None:
            check_and_alert(coin_price)

        # Wait for interval seconds before running again
        time.sleep(INTERVAL_SECONDS - (
            (time.time() - start_time) % INTERVAL_SECONDS))
