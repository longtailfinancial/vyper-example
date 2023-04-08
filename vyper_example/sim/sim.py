import panel as pn
import param as pm
from vyper_example.sim.account import Account

import hvplot.pandas


import pandas as pd
import numpy as np


class Simulation(pm.Parameterized):

    n_accounts = pm.Integer(100, bounds=(0,None))
    accounts = pm.DataFrame(precedence=-1)
    distribution = pm.Selector()

    def __init__(self, distributions: list, **params):
        super(Simulation, self).__init__(**params)
        self.param['distribution'].objects = distributions
        self.distribution = distributions[0]
        self.gen_accounts()

    # @pm.depends('n_accounts', watch=True)
    def _gen_accounts(self, n):
        accounts_list = [Account().param.values() for _ in range(n)]
        accounts = pd.DataFrame(accounts_list)
        self.accounts = accounts

    def _sample_distribution(self, n):
        return self.distribution.df.sample(n=n).sort_index()

    def gen_accounts(self):
        return self._gen_accounts(self.n_accounts)

    def sample_distribution(self):
        return self._sample_distribution(self.n_accounts)

    def view_gen_accounts_table(self, columns=['address', 'balance']):
        return self.accounts[columns].hvplot.table(width=1200)

    def view_sample_distribution_table(self, columns=['address', 'eth_balance']):
        return lambda: self._sample_distribution(self.n_accounts)[columns].hvplot.table()

    def view(self):
        output = pn.Column(

            pn.Row(
                self,
                pn.Column(
                    'Accounts Table',
                    # self.view_gen_accounts_table,
                    self.view_sample_distribution_table,
                )
            )
        )
        return output
