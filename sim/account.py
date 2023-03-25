import param as pm
import secrets
from eth_account import Account
from parameters import Address, Uint256

class Account(pm.Parameterized):

    address = Address()
    key = pm.String()
    balance = Uint256()

    def __init__(self, **params):
        super(Account, self).__init__(**params)
        self.key, self.address = self.generate_eth_account()


    @staticmethod
    def generate_eth_account():
        priv = secrets.token_hex(32)
        private = "0x" + priv
        public = Account.from_key(private).address
        return private, public

