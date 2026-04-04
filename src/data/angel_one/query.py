from SmartApi import SmartConnect
from data.angel_one import constants
from av_core.app import App
from av_core.cred_reader import CredentialsReader
import pyotp

if __name__ == "__main__":
    cred_reader = CredentialsReader('.keys.cnf')
    creds = cred_reader.get_credentials('angel_one')
    api_key = creds[constants.k_API_KEY]
    secret_key = creds[constants.k_SECRET_KEY]
    totp_key = creds[constants.k_TOTP_KEY]
    password = creds[constants.k_PASSWORD]
    user_id = creds[constants.k_USER_ID]

    client = SmartConnect(api_key=api_key)
    try:
        token = totp_key  # In a real implementation, generate TOTP using the totp_key
        totp = pyotp.TOTP(totp_key).now() 
        print(totp)
    except Exception as e:
        print("Error generating TOTP:", e)
        token = None
    session = client.generateSession(user_id, password, totp)
    if(session['status'] == False):
        print("Error generating session:", session)
    else :
        print("Session generated successfully:", session)
    print("Angel One API Client initialized:", client)