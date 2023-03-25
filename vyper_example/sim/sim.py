import panel as pn
import param as pm
from vyper_example.sim.open_auction import OpenAuction
from vyper_example.sim.account import Account

import hvplot.pandas


import pandas as pd
import numpy as np


class View(pm.Parameterized):
    n = 100
    def display(self):

        records = [Account().param.values() for _ in range(self.n)]

        df = pd.DataFrame(records)

        output = pn.Column(
            'account_data', 
            df.hvplot.table(width=1200),
        )

        # output = pd.read_
        a = Account()
        output = df.hvplot.table()


        # account = Account()
        # account_data = dict(account.get_param_values())
        return output





