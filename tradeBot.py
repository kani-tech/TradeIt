import alpaca_trade_api as tradeapi
import numpy as np
import time

SEC_KEY = 'sNMwdDuMeOLBGP2INAw3FzGg7IEEHWStcBAEcFJz'  # Enter Your Secret Key Here
PUB_KEY = 'PKNOXY6PVEUOULTI3V91'  # Enter Your Public Key Here
# This is the base URL for paper trading
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

pos_held = False
# Breakoutlvl
breakoutlvl = None
highest_price = None


class TradeBot:
    def __init__(self, symb):
        self.symb = symb
        self.time_ceiling = 30
        self.floor = 10
        self.backtrack_time = 20
        self.initial_stop_loss = 0.98
        self.trailing_stop_loss = 0.9

    def algo(self):
        market_data = api.get_barset([self.symb], 'day', limit=31)

        closing_data = []
        for bar in market_data[self.symb]:
            closing_data.append(bar.c)

        vol_today = np.std(closing_data[1:31])
        vol_yesterday = np.std(closing_data[1:30])
        change_in_vol = (vol_today - vol_yesterday) / vol_today
        self.backtrack_time = round(self.backtrack_time * (1 + change_in_vol))

        if (self.backtrack_time > self.time_ceiling):
            self.backtrack_time = self.time_ceiling
        elif (self.backtrack_time < self.floor):
            self.backtrack_time = self.time_floor

        daily_highs = []
        for bar in market_data[self.symb]:
            daily_highs.append(bar.h)

        active_positions = api.list_positions()

        position_exists = active_positions.__contains__(self.symb)
        # No position has been owned and the most recent close price is greater than the last 30 days max price so buy
        if not position_exists and closing_data[-1] >= max(daily_highs[:-1]):
            print("Buy")
            api.submit_order(
                symbol='SPY',
                qty=1,
                side="buy",
                type="market",
                time_in_force='gtc'
            )
            self.breakoutlvl = max(daily_highs[:-1])
            self.highestPrice = self.breakoutlvl

        if (len(api.list_orders("open"))):
            self.stop_receipt =


myBot = TradeBot("SPY")
myBot.algo()
""" while True:
    print("")
    print("Checking Price")
    market_data = api.get_barset([symb], 'day', limit=31)
    print(market_data)

    # Time Values
    time_ceiling = 30
    time_floor = 10
    backtrack_time = 20

    # Stop Losses
    initial_stop_loss = 0.98
    trailing_stop_risk = 0.9

    # Find the closing price for the past 30 dalys
    closing_data = []
    for bar in market_data[symb]:
        closing_data.append(bar.c)

    vol_today = np.std(closing_data[1:31])
    vol_yesterday = np.std(closing_data[1:30])
    change_in_vol = (vol_today - vol_yesterday) / vol_today
    backtrack_time = round(backtrack_time * (1 + change_in_vol))

    if (backtrack_time > time_ceiling):
        backtrack_time = time_ceiling
    elif (backtrack_time < time_floor):
        backtrack_time = time_floor

    daily_highs = []
    for bar in market_data[symb]:
        daily_highs.append(bar.h)

    # No position has been owned and the most recent close price is greater than the last 30 days max price so buy
    if not pos_held and closing_data[-1] >= max(daily_highs[:-1]):
        print("Buy")
        api.submit_order(
            symbol='SPY',
            qty=1,
            side="buy",
            type="market",
            time_in_force='gtc'
        )
        pos_held = True
        breakoutlvl = max(daily_highs[:-1])
        highest_price = breakoutlvl

    if (pos_held):
        if not api.list_orders(status="open"):
            print("data", market_data[symb])
    print("close", closing_data)
    print("highs", daily_highs)

    time.sleep(60)
 """
