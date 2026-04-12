ANGEL_ONE = 'angel_one_smartapi'

k_API_KEY = 'api_key'
k_SECRET_KEY = 'secret_key'
k_TOTP_KEY = 'totp_key'
k_PASSWORD = 'password'
k_USER_ID = 'user_id'


INSTRUMENTS_URL = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

INSTRUMENTS_CACHE_PATH = '/opt/jazz/data/quantquill/smartapi/instruments/'


# Instrument field keys
k_TOKEN = 'token'
k_SYMBOL = 'symbol'
k_NAME = 'name'
k_EXPIRY = 'expiry'
k_STRIKE = 'strike'
k_LOTSIZE = 'lotsize'
k_INSTRUMENTTYPE = 'instrumenttype'
k_EXCH_SEG = 'exch_seg'

CANDLE_INFO_MAX_DAYS = {
    "ONE_MINUTE": 30,
    "THREE_MINUTE": 60,
    "FIVE_MINUTE": 100,
    "TEN_MINUTE": 100,
    "FIFTEEN_MINUTE": 200,
    "THIRTY_MINUTE": 200,
    "ONE_HOUR": 400,
    "ONE_DAY": 2000
}