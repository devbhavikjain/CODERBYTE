from flask import request,Flask,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from datetime import datetime as dt

from db_operations import DB

# Logging
import logging
logging.basicConfig(format='%(asctime)s -  %(levelname)s - %(message)s')
logger = logging.getLogger('api')
logger.setLevel(logging.INFO)

def load_coin_data(date_str, sql_offset, sql_limit):
    """
    Loads Coin data from DB in formatted manner
    Args:
        date_str (str) : Date string in DD-MM-YYYY format
        sql_offset (int) : for pagination that indicates whats the offset
            entry from where the rows need to start
        sql_limit (str) : for pagination that indicates how many rows
            that need to be returned
    Returns:
        list: formmatted records as list of dicts
        int: number of records fetched
    """
    query = """SELECT
    CAST(price AS INT),
    strftime(?, utctime)
    FROM bitcoin
    WHERE strftime(?, utctime) = ?
    LIMIT ? offset ?"""

    # Control input and output date format as required
    output_format = '%Y-%m-%d %H:%M:%S'
    inp_date_format = '%d-%m-%Y'

    params = [output_format, inp_date_format, date_str, sql_limit, sql_offset]
    sql_obj = DB('crypto.db')
    results = sql_obj.execute_and_fetch(query, params)

    # Format the results into array of JSONs
    formatted_data = [{
        "price" : row[0],
        "timestamp" : row[1],
        "coin" : "btc"
        } for row in results]
    num_records = len(formatted_data)

    return formatted_data, num_records

@app.route('/api/prices/btc', methods=['POST', 'GET'])
def bitcoin_api():
    """
    Used to query the database for price data for given date and offset range
    parameters:
      - name: date
        in: query
        type: string
        required: true
        description: date in DD-MM-YYYY
      - name: limit
        in: query
        type: integer
        description: for pagination that indicates how many rows that need to be returned
      - name: offset
        in: query
        type: integer
        description: for pagination that indicates whats the offset entry from where the rows need to start
    """
    logger.info("Serving request..")

    # Load and Parse the arguments
    req_parameters = request.args.to_dict()
    req_date = req_parameters.get('date', None)
    req_limit = int(req_parameters.get('limit', 10))
    req_offset = int(req_parameters.get('offset', 0))

    if req_date is None:
        ret_obj = {
            "Flag":False,
            "Message": "Missing a valid Date in DD-MM-YYYY format"
            }
        return jsonify(ret_obj)
        

    # Save current url
    current_url = request.url

    # Build the next url
    next_url = request.base_url
    next_url += f"?date={req_date}"
    next_url += f"&offset={req_offset + req_limit}"
    next_url += f"&limit={req_limit}"

    formatted_results, total_count = load_coin_data(
        req_date, req_offset, req_limit)

    return_obj = {
        "url"   : f"<{current_url}>",
        "next"  : f"<{next_url}>",
        "count" : total_count,
        "data"  : formatted_results
        }
    return jsonify(return_obj)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
