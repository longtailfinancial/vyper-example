import panel as pn
import param as pm
import pandas as pd
import secrets
from eth_account import Account as ETH_Account
from vyper_example.sim.parameters import Address
from vyper_example.sim.ledger import Ledger
from icecream import ic

class Account(pm.Parameterized):

    address = Address()
    key = pm.String(precedence=-1)
    balance = pm.Number(0, bounds=(0,None))
    ledger = pm.ClassSelector(class_=Ledger, precedence=-1)

    def __init__(self, ledger: Ledger, **params):
        super(Account, self).__init__(**params)
        self.ledger = ledger
        self.key, self.address = self.generate_eth_account()
        self.ledger.df = pd.concat(
            [
                self.ledger.df, 
                pd.DataFrame([{'eth_balance': self.balance}], index=pd.Series([self.address], name='address')),
            ])

    def send(self, account, pending_amount):
        assert self.balance >= pending_amount
        self.ledger.send(self.address, account.address, pending_amount)
        self.balance -= pending_amount
        account.balance += pending_amount

    def __str__(self):
        return self.address

    def __repr__(self):
        return self.address

    @staticmethod
    def generate_eth_account():
        private = "0x" + secrets.token_hex(32)
        public = ETH_Account.from_key(private).address
        return private, public

    def view(self):
        return pn.panel(self)

class Contract(Account):
    pass
