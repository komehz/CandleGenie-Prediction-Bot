import datetime as dt
from web3 import Web3
from web3.middleware import geth_poa_middleware
from config import *
from colorama import init
from colorama import Fore, Back, Style
import time


# For colorama
init()

w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

ADDRESS = w3.toChecksumAddress(ADDRESS)
PRIVATE_KEY = str(PRIVATE_KEY).lower()

# TX SETTING
GAS = 400000
GAS_WIN = 800000
GAS_PRICE = 5000000000

# Seconds left to new bet
SECONDS_LEFT = 20

# For Conversions
div = 100_000_000
div2 = 1_000_000_000_000_000_000

# Data storage
st = []
wl = []


class Prediction:

    def __init__(self, contract, abi):
        # CONTRACT
        self.predictionContract = w3.eth.contract(address=contract, abi=abi)
        self.length = self.predictionContract.functions.getUserRoundsLength(ADDRESS).call()

    def bet_bull(self, value, epoch):
        try:
            bull_bet = self.predictionContract.functions.BetBull(epoch).buildTransaction({
                'from': ADDRESS,
                'nonce': w3.eth.getTransactionCount(ADDRESS),
                'value': value,
                'gas': GAS,
                'gasPrice': GAS_PRICE,
            })
            signed_tx = w3.eth.account.signTransaction(bull_bet, private_key=PRIVATE_KEY)
            w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(f'{w3.eth.waitForTransactionReceipt(signed_tx.hash)}')
        except Exception as e:
            print(Fore.RED + f'Bet Bull fail - {e}')
            print(Fore.RESET)

    def bet_bear(self, value, epoch):
        try:
            bear_bet = self.predictionContract.functions.BetBear(epoch).buildTransaction({
                'from': ADDRESS,
                'nonce': w3.eth.getTransactionCount(ADDRESS),
                'value': value,
                'gas': GAS,
                'gasPrice': GAS_PRICE,
            })
            signed_tx = w3.eth.account.signTransaction(bear_bet, private_key=PRIVATE_KEY)
            w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(f'{w3.eth.waitForTransactionReceipt(signed_tx.hash)}')
        except Exception as e:
            print(Fore.RED + f'Bet Bear fail - {e}')
            print(Fore.RESET)

    def make_bet(self, epoch, direction):
        try:
            value = w3.toWei(BET_AMOUNT, 'ether')
            if direction == 'STRONG BUY':
                print(Back.GREEN + f'Going Bull #{epoch} | {BET_AMOUNT} BNB  ')
                print(Back.RESET)
                self.bet_bull(value, epoch)
            elif direction == 'STRONG SELL':
                print(Back.RED + f'Going Bear #{epoch} | {BET_AMOUNT} BNB  ')
                print(Back.RESET)
                self.bet_bear(value, epoch)
        except Exception as e:
            print(Fore.RED + f'Make Bet fail - {e}')
            print(Fore.RESET)

    def new_round(self):
        try:
            current = self.predictionContract.functions.currentEpoch().call()
            data = self.predictionContract.functions.Rounds(current).call()
            start_time = dt.datetime.fromtimestamp(data[8]) - dt.timedelta(seconds=SECONDS_LEFT)
            print(Back.WHITE)
            print(Fore.BLACK + '==========*' * 20)
            print(Style.RESET_ALL)
            print(Fore.MAGENTA + f'New round: #{current}')
            print(Fore.RESET)
            return [start_time, current]
        except Exception as e:
            print(Fore.RED + f'New round fail - {e}')
            print(Fore.RESET)

    def claim(self, epoch):
        try:
            c = self.predictionContract.functions.Claim(epoch).buildTransaction({
                'from': ADDRESS,
                'nonce': w3.eth.getTransactionCount(ADDRESS),
                'value': 0,
                'gas': GAS_WIN,
                'gasPrice': GAS_PRICE,
            })
            signed_tx = w3.eth.account.signTransaction(c, private_key=PRIVATE_KEY)
            w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(f'{w3.eth.waitForTransactionReceipt(signed_tx.hash)}')

        except Exception as e:
            print(Fore.RED + f'Claim fail: {e}')
            print(Fore.RESET)

    def refund(self, epoch):
        try:
            d = self.predictionContract.functions.Refund(epoch).buildTransaction({
                'from': ADDRESS,
                'nonce': w3.eth.getTransactionCount(ADDRESS),
                'value': 0,
                'gas': GAS,
                'gasPrice': GAS_PRICE,
            })
            signed_tx = w3.eth.account.signTransaction(d, private_key=PRIVATE_KEY)
            w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(f'{w3.eth.waitForTransactionReceipt(signed_tx.hash)}')

        except Exception as e:
            print(Fore.RED + f'Refund fail: {e}')
            print(Fore.RESET)

    def claim_and_refund(self):
        try:
            wins = []
            refunds = []
            end = self.predictionContract.functions.getUserRoundsLength(ADDRESS).call()
            user_rounds = self.predictionContract.functions.getUserRounds(ADDRESS, (self.length-2), end+2).call()
            self.length = end
            for epk in user_rounds[0]:
                claimable = self.predictionContract.functions.claimable(epk, ADDRESS).call()
                refundable = self.predictionContract.functions.refundable(epk, ADDRESS).call()
                if claimable:
                    wins.append(epk)
                elif refundable:
                    refunds.append(epk)

            self.claim(wins)
            time.sleep(20)
            if refunds:
                self.refund(refunds)
            else:
                print(f'No refund available: {refunds}')

            print(f'\nNumber of games: {len(user_rounds[0])}')
            print(f'Wins: {wins} || Number of wins: {len(wins)}')
            print(f'Refunds: {refunds} || Number of refunds: {len(refunds)}')
            print(Back.BLUE + f'Win rate: {round((len(wins)/(len(user_rounds[0])-len(refunds)))*100, 2)}%')
            print(Back.RESET)

        except Exception as e:
            print(Fore.RED + f'Claim/Refund fail - {e}')
            print(Fore.RESET)

    def data(self):
        try:
            data = self.predictionContract.functions.getUserRounds(ADDRESS, self.length, 1000).call()

            epk = data[0]
            for i in range(len(data[1])):
                _, a, _, _, b = data[1][i]
                st.append(a)
                wl.append(b)

            data = {
                "lock time": st,
                "epoch": epk,
                "Win/Lose": wl
            }
            return data
        except Exception as e:
            print(Fore.RED + f'Data fail - {e}')
            print(Fore.RESET)
