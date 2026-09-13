from quantquill import av_core
from alpha_server.main import start_alpha_server
import configparser


class AlphaServer(av_core.app.App):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./configs/start_alpha_server.py.cnf')
        self.port = config.getint('server', 'port', fallback=8091)
    
    def start(self):
        start_alpha_server(self.port)


def main():
    AlphaServer().start()

if(__name__ == "__main__"):
    main()