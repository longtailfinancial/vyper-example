import panel as pn
import holoviews as hv
from vyper_example.sim.open_auction import OpenAuction
from vyper_example.sim.account import Account
from vyper_example.sim.sim import Simulation
from vyper_example.sim.distributions import Distribution


pn.extension()
hv.extension("bokeh")

ACCENT_COLOR = "#00286e"
SITE = "Vyper Example"
TITLE = "Simulations"

account = Account()
open_auction = OpenAuction(beneficiary=account.address)

models_row = pn.Row(
    account.view,
    open_auction.view,
)

models_pane = pn.Column(
    '# Models',
    models_row,
)

distribution1 = Distribution()
distribution2 = Distribution()

sim_pane = pn.Column(
    '# Simulation',
    Simulation(distributions=[distribution1, distribution2]).view,
)

apps = [
    sim_pane,
    models_pane,
]



def app():
    return pn.template.FastListTemplate(
        site=SITE,
        title=TITLE,
        header_background=ACCENT_COLOR,
        main=apps,
    ).servable()


app()
