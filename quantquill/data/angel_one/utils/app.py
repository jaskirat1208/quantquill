from typing import Optional
import pyotp

from quantquill.av_core import app as av_core
from quantquill.av_core.cred_reader import CredentialsReader
from quantquill.data.angel_one.utils import constants
from quantquill.data.angel_one.utils.SmartAPIWithInstruments import SmartConnect


class AngelOneSmartApp(av_core.App):
    def __init__(self, config_file: Optional[str] = None, log_file: Optional[str] = None, instance_name: str = ""):
        super().__init__(config_file=config_file, log_file=log_file, instance_name=instance_name)
        keys_file = self.config['DEFAULT'].get('keys_file', '.keys.cnf')
        cred_reader = CredentialsReader(keys_file)
        creds = cred_reader.get_credentials('angel_one')
        self.m_api_key = creds[constants.k_API_KEY]
        self.m_totp_key = creds[constants.k_TOTP_KEY]
        self.m_password = creds[constants.k_PASSWORD]
        self.m_user_id = creds[constants.k_USER_ID]

        self.m_client = SmartConnect(api_key=self.m_api_key)
        self.logger.info("ABSmartApp initialized with credentials for Angel One API.")
        # You can now use the client with the generated session for further API calls    
        self.create_session()

    def create_session(self):
        """
        Create a session for the user. This involves generating a TOTP (Time-based One-Time Password) using the provided TOTP key and then using it to authenticate with the Angel One API to generate a session.
        """
        self.logger.info(f"Creating session for user: {self.m_user_id}. Generating TOTP...")

        totp = pyotp.TOTP(self.m_totp_key).now()
        self.logger.info(f"Generated TOTP for session") 
        self.session = self.m_client.generateSession(self.m_user_id, self.m_password, totp)

        # Check if session generation was successful. Raises exception if some error occurred during session generation. Otherwise, logs the successful session generation and the obtained JWT and refresh tokens.
        if self.session['status'] == False:
            self.logger.error(f"Error generating session: {self.session}")
            raise Exception(f"Failed to create session: {self.session}")

        # Session generated successfully, log the session details and extract the JWT and refresh tokens for further use.
        self.logger.info(f"Session generated successfully: {self.session}")
        self.m_jwt_tok = self.session['data']['jwtToken']
        self.logger.info(f"JWT Token: {self.m_jwt_tok}")
        self.m_refreshToken = self.session['data']['refreshToken']
        self.logger.info(f"Refresh Token: {self.m_refreshToken}")
        res = self.m_client.getProfile(self.m_refreshToken)
        self.m_client.generateToken(self.m_refreshToken)
        self.logger.info(f"Profile data: {res}")


    def start(self):
        self.logger.info("ABSmartApp started.")

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

    def get_client(self):
        return self.m_client

    def get_logger(self):
        return self.logger

if(__name__ == "__main__"):
    app = AngelOneSmartApp()
    app.start()
    app.stop()
