from typing import Optional
import pyotp
import json
import os
from datetime import datetime, timedelta

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
        # Try to load cached session first, otherwise create new session
        if not self._load_cached_session():
            self.create_session()

    def _get_session_cache_path(self):
        """Get the path to the session cache file for this user."""
        os.makedirs(constants.SESSION_CACHE_PATH, exist_ok=True)
        return os.path.join(constants.SESSION_CACHE_PATH, f"session_{self.m_user_id}.json")

    def _load_cached_session(self):
        """Load cached session if it exists and is valid."""
        cache_path = self._get_session_cache_path()
        
        if not os.path.exists(cache_path):
            self.logger.info("No cached session found. Will create new session.")
            return False
        
        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
            
            # Check if cached session is for the same user
            if cached_data.get('user_id') != self.m_user_id:
                self.logger.warning("Cached session is for different user. Will create new session.")
                return False
            
            # Check if session is expired (JWT tokens typically expire in 24 hours)
            cache_time = datetime.fromisoformat(cached_data.get('timestamp', ''))
            if datetime.now() - cache_time > timedelta(hours=23):
                self.logger.info("Cached session expired. Will create new session.")
                return False
            
            # Load cached tokens
            self.m_jwt_tok = cached_data.get('jwt_token')
            self.m_refreshToken = cached_data.get('refresh_token')
            
            # Set tokens in client
            self.m_client.access_token = self.m_jwt_tok
            self.m_client.refresh_token = self.m_refreshToken
            self.m_client.userId = self.m_user_id
            
            # Verify session is still valid by making a lightweight API call
            try:
                res = self.m_client.getProfile(self.m_refreshToken)
                self.logger.info(f"Cached session is valid. Profile data: {res}")
                return True
            except Exception as e:
                self.logger.warning(f"Cached session invalid: {e}. Will create new session.")
                # Clear invalid cache to force fresh session on next attempt
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                    self.logger.info(f"Cleared invalid session cache: {cache_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading cached session: {e}. Will create new session.")
            return False

    def _save_session_to_cache(self):
        """Save current session tokens to cache."""
        cache_path = self._get_session_cache_path()
        
        try:
            cache_data = {
                'jwt_token': self.m_jwt_tok,
                'refresh_token': self.m_refreshToken,
                'user_id': self.m_user_id,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
            
            self.logger.info(f"Session cached successfully to: {cache_path}")
        except Exception as e:
            self.logger.error(f"Error saving session to cache: {e}")

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
        
        # Save session to cache for future use
        self._save_session_to_cache()


    def start(self):
        self.logger.info("ABSmartApp started.")

    def stop(self):
        self.logger.info("ABSmartApp stopping. Cleaning up resources...")
        try:
            self.logger.info(f"Logging out user: {self.m_user_id}")
            self.m_client.terminateSession(self.m_user_id)
            self.logger.info("Session terminated successfully.")
            
            # Clear cached session on logout
            cache_path = self._get_session_cache_path()
            if os.path.exists(cache_path):
                os.remove(cache_path)
                self.logger.info("Cached session cleared.")
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
