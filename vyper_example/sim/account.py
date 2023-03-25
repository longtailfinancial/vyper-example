import panel as pn
import param as pm
import secrets
from eth_account import Account as ETH_Account
from vyper_example.sim.parameters import Address, Uint256

class Account(pm.Parameterized):

    address = Address()
    key = pm.String(precedence=-1)
    balance = Uint256()

    def __init__(self, **params):
        super(Account, self).__init__(**params)
        self.key, self.address = self.generate_eth_account()


    @staticmethod
    def generate_eth_account():
        private = "0x" + secrets.token_hex(32)
        public = ETH_Account.from_key(private).address
        return private, public


class View(pm.Parameterized):
    def display(self):
        account = Account()
        return pn.panel(account)


