from quantquill import av_core
from alpha_server.main import start_alpha_server
import configparser
import sys


class AlphaServer(av_core.app.App):
    def __init__(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        self.port = config.getint('server', 'port', fallback=8091)
    
    def start(self):
        start_alpha_server(self.port)


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else './configs/start_alpha_server.py.cnf'
    AlphaServer(config_path).start()

if(__name__ == "__main__"):
    main()