from massive import RESTClient
from quantquill.av_core.cred_reader import CredentialsReader
import time
import requests

class RateLimitedRESTClient(RESTClient):
    def __init__(self, api_key, rate_limit_per_minute=5, **kwargs):
        super().__init__(api_key, **kwargs)
        self.rate_limit_per_minute = rate_limit_per_minute
        self.last_call_time = 0
        self.min_interval = 60 / rate_limit_per_minute  # seconds between calls

    def _get(self, *args, **kwargs):
        # Wait if necessary to respect rate limit
        elapsed = time.time() - self.last_call_time
        while elapsed < self.min_interval:
            print(f"Waiting {self.min_interval - elapsed:.2f} seconds to respect rate limit...")
            time.sleep(1)
            elapsed = time.time() - self.last_call_time

        
        self.last_call_time = time.time()
        
        try:
            return super()._get(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                # If we still get 429, wait longer
                print("Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                return super()._get(*args, **kwargs)
            else:
                raise


def get_api_client(**kwargs):
    cred_reader = CredentialsReader('.keys.cnf')
    creds = cred_reader.get_credentials('massive_api')
    return RateLimitedRESTClient(a            )

