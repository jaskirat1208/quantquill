from quantquill import av_core
from alpha_server.main import start_alpha_server


class AlphaServer(av_core.app.App):
    def __init__(self):
        pass
    
    def start(self):
        start_alpha_server()


def main():
    AlphaServer().start()

if(__name__ == "__main__"):
    main()