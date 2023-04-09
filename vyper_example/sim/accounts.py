import panel as pn
import param as pm
import secrets
from eth_account import Account as ETH_Account
from vyper_example.sim.parameters import Address
from vyper_example.sim.ledger import Ledger

class Account(pm.Parameterized):

    address = Address()
    key = pm.String(precedence=-1)
    balance = pm.Number(0, bounds=(0,None))
    ledger = pm.ClassSelector(class_=Ledger, precedence=-1)

    def __init__(self, ledger: Ledger, **params):
        super(Account, self).__init__(**params)
        self.key, self.address = self.generate_eth_account()
        self.ledger = ledger

    @staticmethod
    def generate_eth_account():
        private = "0x" + secrets.token_hex(32)
        public = ETH_Account.from_key(private).address
        return private, public

    def view(self):
        return pn.panel(self)


class Contract(Account):

    def send(self, address, pending_amount):
        self.ledger.df.loc[self.address]["eth_balance"] -= pending_amount
        self.ledger.df.loc[address]["eth_balance"] += pending_amount



