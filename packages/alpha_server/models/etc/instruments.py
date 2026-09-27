from quantquill.data.angel_one.utils import SmartAPIWithInstruments  as SmartApi

# Singleton instance of SmartConnect
_smart_connect_instance = None

def get_smart_connect():
    """Get or create the singleton SmartConnect instance."""
    global _smart_connect_instance
    if _smart_connect_instance is None:
        _smart_connect_instance = SmartApi.SmartConnect()
    return _smart_connect_instance

def get_instruments():
    api = get_smart_connect()
    symbolInfo = api.symbol_map
    return list(symbolInfo.values())

def get_instrument_info():
    pass

def getInstrumentsByUnderlying(underlying: str):
    api = get_smart_connect()
    return api.getInstrumentsByUnderlying(underlying)

def __main__():
    instruments = get_instruments()
    print(f"Loaded {len(instruments)} instruments")
    print(instruments)


if __name__ == "__main__":
    __main__()