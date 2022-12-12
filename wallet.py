from web3 import Web3
from web3.middleware import geth_poa_middleware


w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

ADDRESS = w3.toChecksumAddress("fill in your wallet address here")


def my_balance():
    balance = w3.fromWei(w3.eth.get_balance(ADDRESS), 'ether')
    return balance
