from av_core.av_cred_reader import CredentialsReader
from alpha_vantage.query import AlphaVantageClient

if __name__ == "__main__":
    cred_reader = CredentialsReader('.keys.cnf')
    credentials = cred_reader.get_credentials('alpha_vantage')
    api_key = credentials['api_key']
    client = AlphaVantageClient(api_key)
    print("API Key:", api_key)
