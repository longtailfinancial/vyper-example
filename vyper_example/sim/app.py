import panel as pn
import holoviews as hv
from vyper_example.sim.open_auction import OpenAuction
from vyper_example.sim.account import Account
from vyper_example.sim.sim import Simulation


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

sim_pane = pn.Column(
    '# Simulation',
    Simulation().view,
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
