import configparser
import os

class CredentialsReader: 
    def __init__(self, filename, file_path=''):
        if(not file_path):
            file_path = os.path.expanduser('~')
        self.file_path = file_path + '/' + filename
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path)

    def get_credentials(self, section):
        if section in self.config:
            return dict(self.config.items(section))
        else:
            raise ValueError(f"Section '{section}' not found in the configuration file.")
        
    def getConfig(self):
        return self.config


# Example usage:
if __name__ == "__main__":
    cred_reader = CredentialsReader('.keys.cnf')
    credentials = cred_reader.get_credentials('alpha_vantage')
    print(credentials['api_key'])
