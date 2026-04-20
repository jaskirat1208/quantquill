from quantquill.data.angel_one.utils import SmartAPIWithInstruments  as SmartApi

def get_instruments():
    api = SmartApi.SmartConnect()
    symbolInfo = api.symbol_map
    return list(symbolInfo.values())

def get_instrument_info():
    pass


def __main__():
    instruments = get_instruments()
    print(f"Loaded {len(instruments)} instruments")
    print(instruments)


if __name__ == "__main__":
    __main__()