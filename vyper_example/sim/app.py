import panel as pn
import holoviews as hv
from vyper_example.sim.open_auction import OpenAuction, Bid
from vyper_example.sim.account import Account
from vyper_example.sim.sim import Simulation
from vyper_example.sim.distributions import Distribution
import datetime as dt


pn.extension()
hv.extension("bokeh")

ACCENT_COLOR = "#00286e"
SITE = "Vyper Example"
TITLE = "Simulations"

beneficiary_account = Account()
bidding_account = Account(balance=10)

auction_start = dt.datetime.now() 
auction_start = auction_start.replace(second=0, microsecond=0, minute=0, hour=auction_start.hour)
auction_start = int(auction_start.timestamp())
bidding_time = 60*60


open_auction = OpenAuction(
    beneficiary=beneficiary_account.address, 
    auction_start=auction_start,
    bidding_time=bidding_time,
)

bid = Bid(
    value=5,
    timestamp= int(dt.datetime.now().timestamp()),
    sender = bidding_account.address,
    open_auction=open_auction,
)

models_row = pn.Row(
    beneficiary_account.view,
    open_auction.view,
    bid,
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
