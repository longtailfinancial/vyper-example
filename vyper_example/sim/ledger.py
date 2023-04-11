import pandas as pd
import panel as pn
import param as pm
import os
import hvplot.pandas
from icecream import ic

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT_DIR, 'data/')
SAMPLE_PERCENT = 0.01

sample_every_n_rows: int = int((1 / SAMPLE_PERCENT) * 100)

class Ledger(pm.Parameterized):

    df = pm.DataFrame()

    def __init__(self, **params):
        super(Ledger, self).__init__(**params)
        self.df = pd.read_csv(
            os.path.join(DATA_DIR, 'eth_balances_small.csv'), 
            header=0, 
            skiprows=lambda i: i % sample_every_n_rows != 0,
            index_col='address',
            usecols=['address', 'eth_balance'],
        )

    def send(self, from_address: str, to_address: str, pending_amount):
        assert self.df.at[from_address, "eth_balance"] >= pending_amount
        self.df.at[from_address, "eth_balance"] -= pending_amount
        self.df.at[to_address, "eth_balance"] += pending_amount
        self.param.trigger('df')

    def view(self):
        # ic(self.df)
        return self.df.reset_index().hvplot.table()


