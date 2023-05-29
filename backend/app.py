from traceback import format_exc
from flask import Flask, request
from flask_cors import CORS
from loguru import logger
from utils import fetch_list

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    searchterm = request.args.get('searchterm', None)
    logger.debug(f'searchterm: {searchterm}')
    if not searchterm:
        return []
    try:
        return fetch_list(searchterm)
    except Exception as _e:
        logger.critical(str(_e))
        logger.critical(str(format_exc()))
        return {'status': 'error'}
