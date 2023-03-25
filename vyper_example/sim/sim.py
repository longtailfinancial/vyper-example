import panel as pn
import param as pm
from vyper_example.sim.open_auction import OpenAuction
from vyper_example.sim.account import Account

import hvplot.pandas


import pandas as pd
import numpy as np


class Simulation(pm.Parameterized):

    n_accounts = pm.Integer(100, bounds=(0,None))
    accounts = pm.DataFrame()

    def __init__(self, **params):
        super(Simulation, self).__init__(**params)
        self.accounts = self._gen_accounts()

    def _gen_accounts(self) -> pd.DataFrame:
        records = [Account().param.values() for _ in range(self.n_accounts)]
        df = pd.DataFrame(records)[['address', 'balance']]
        return df

    def view(self):
        accounts_table = self.accounts.hvplot.table(width=1200)
        output = pn.Column(
            'Accounts Table',
            accounts_table,
        )
        return output
