from typing import Optional
import pyotp

from SmartApi import SmartConnect
from av_core import app as av_core
from av_core.cred_reader import CredentialsReader
from data.angel_one import constants

class ABSmartApp(av_core.App):
    def __init__(self, config_file: Optional[str] = None, log_file: Optional[str] = None, instance_name: str = ""):
        self.app = av_core.App(config_file=config_file, log_file=log_file, instance_name=instance_name)
        self.logger = self.app.logger

        cred_reader = CredentialsReader('.keys.cnf')
        creds = cred_reader.get_credentials('angel_one')
        self.m_api_key = creds[constants.k_API_KEY]
        self.m_secret_key = creds[constants.k_SECRET_KEY]
        self.m_totp_key = creds[constants.k_TOTP_KEY]
        self.m_password = creds[constants.k_PASSWORD]
        self.m_user_id = creds[constants.k_USER_ID]

        self.m_client = SmartConnect(api_key=self.m_api_key)
        self.logger.info("ABSmartApp initialized with credentials for Angel One API.")

    def create_session(self):
        self.logger.info(f"Creating session for user: {self.m_user_id}. Generating TOTP...")

        totp = pyotp.TOTP(self.m_totp_key).now()
        self.logger.info(f"Generated TOTP: {totp}") 
        self.session = self.m_client.generateSession(self.m_user_id, self.m_password, totp)

    def start(self):
        self.logger.info("ABSmartApp started.")
        
        self.create_session()
        # Initialize any necessary resources or subscriptions here
        if self.session['status'] == False:
            self.logger.error(f"Error generating session: {self.session}")
        else:
            self.logger.info(f"Session generated successfully: {self.session}")
        
            self.m_tok = self.session['data']['jwtToken']
            self.logger.info(f"JWT Token: {self.m_tok}")
            self.m_refreshToken = self.session['data']['refreshToken']
            self.logger.info(f"Refresh Token: {self.m_refreshToken}")
            res = self.m_client.getProfile(self.m_refreshToken)
            self.m_client.generateToken(self.m_refreshToken)
            print(res)

            # You can now use the client with the generated session for further API calls    

    def stop(self):
        self.logger.info("ABSmartApp stopping. Cleaning up resources...")
        try:
            self.logger.info(f"Logging out user: {self.m_user_id}")
            self.m_client.terminateSession(self.m_user_id)
            self.logger.info("Session terminated successfully.")
        except Exception as e:
            self.logger.error(f"Error occurred while logging out: {e}")
        # Clean up any resources, close connections, etc. here
        self.logger.info("ABSmartApp stopped.")

if(__name__ == "__main__"):
    app = ABSmartApp()
    app.start()
    app.stop()
