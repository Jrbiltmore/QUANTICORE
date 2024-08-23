
from web3 import Web3

def connect_to_blockchain():
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    return w3.isConnected()
