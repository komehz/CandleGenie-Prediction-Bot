import time
import datetime as dt
import sys
from trading import Trading
from prediction import Prediction
from contract import *
from wallet import my_balance
from config import BET_AMOUNT
import telegram_send

ADDRESS_BNB = 'https://www.tradingview.com/symbols/BNBUSDT/technicals/?exchange=BINANCE'
ADDRESS_BTC = 'https://www.tradingview.com/symbols/BTCUSDT/technicals/?exchange=BINANCE'

direction = Trading(ADDRESS_BNB)
BNB = Prediction(PREDICTION_CONTRACT_BNB, PREDICTION_ABI_BNB)

new_round = BNB.new_round()
playing = True
count = 0
summary = [0, 0]
price = [0, 0]

while playing:
    try:
        now = dt.datetime.now()
        if now >= new_round[0]:
            print(f'Played: {count}')
            a, b = direction.summary()
            summary.append(a)
            summary.pop(0)
            price.append(b)
            price.pop(0)
            change = price[1] - price[0]

            print(summary)
            print(price)

            # if (change >= 1.4) and (change < 10):
            #     BNB.make_bet(new_round[1], 'STRONG SELL')
            #     print(f'Price change round with a change of: ${change}')
            #     time.sleep(240)
            #     count += 1
            #     new_round = BNB.new_round()
            if (summary[0] == 'STRONG BUY') or (summary[0] == 'STRONG SELL'):
                BNB.make_bet(new_round[1], summary[0])
                time.sleep(240)
                count += 1
                new_round = BNB.new_round()
            else:
                time.sleep(240)
                new_round = BNB.new_round()
            if my_balance() <= BET_AMOUNT*1.5:
                BNB.claim_and_refund()
                time.sleep(10)
                print(f'\nWallet balance: {my_balance()} BNB')
                telegram_send.send(messages=[f'Wallet balance: {round(my_balance(), 4)} BNB'])
                new_round = BNB.new_round()
        else:
            time.sleep(1)
    except Exception as e:
        print(f"Something wrong: {e}")
        telegram_send.send(messages=[f'Something wrong: {e}'])
        time.sleep(10)
        telegram_send.send(messages=['Done'])
        sys.exit()
