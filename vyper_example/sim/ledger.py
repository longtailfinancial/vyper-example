import pandas as pd
import panel as pn
import param as pm
import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT_DIR, 'data/')
SAMPLE_PERCENT = 1

sample_every_n_rows: int = int((1 / SAMPLE_PERCENT) * 100)

class Ledger(pm.Parameterized):

    df = pd.read_csv(
        os.path.join(DATA_DIR, 'eth_balances_small.csv'), 
        header=0, 
        skiprows=lambda i: i % sample_every_n_rows != 0,
    )[['address', 'eth_balance']]


    def view(self):
        return self.df.head()


