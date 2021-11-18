import alpaca_trade_api as tradeapi
import numpy as np
import time

SEC_KEY = 'sNMwdDuMeOLBGP2INAw3FzGg7IEEHWStcBAEcFJz'  # Enter Your Secret Key Here
PUB_KEY = 'PKNOXY6PVEUOULTI3V91'  # Enter Your Public Key Here
# This is the base URL for paper trading
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

symb = "SPY"
pos_held = False

while True:
    print("")
    print("Checking Price")
    market_data = api.get_barset([symb], 'day', limit=31)
    print(market_data)
    backtrack_time = 20

    # Find the closing price for the past 30 dalys
    closing_data = []
    for bar in market_data[symb]:
        closing_data.append(bar.c)

    vol_today = np.std(closing_data[1:31])
    vol_yesterday = np.std(closing_data[1:30])
    change_in_vol = (vol_today - vol_yesterday) / vol_today
    backtrack_time = round(backtrack_time * (1 + change_in_vol))

    """ close_list = []
    for bar in market_data[symb]:
        close_list.append(bar.c)

    close_list = np.array(close_list, dtype=np.float64)
    ma = np.mean(close_list)
    last_price = close_list[4]

    print("Moving Average " + str(ma))
    last_price = close_list[4]

    print("Moving Average " + str(ma))
    print("Last Price" + str(last_price))

    if ma + 0.1 < last_price and not pos_held:
        print("Buy")
        api.submit_order(
            symbol='SPY',
            qty=1,
            side="buy",
            type="market",
            time_in_force='gtc'
        )
        pos_held = True
    elif ma + 0.1 < last_price and not pos_held:
        print("Sell $")
        api.submit_order(
            symbol='SPY',
            qty=1,
            side="sell",
            type="market",
            time_in_force='gtc'
        )
        pos_held = False """

    time.sleep(60)
