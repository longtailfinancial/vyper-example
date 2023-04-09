import panel as pn
import holoviews as hv
from vyper_example.sim.open_auction import OpenAuction, Bid, Withdraw
from vyper_example.sim.accounts import Account
from vyper_example.sim.ledger import Ledger
from vyper_example.sim.sim import Simulation
import datetime as dt
from icecream import ic
pn.extension()
hv.extension("bokeh")

# Use Icecream for Logging
ic("🌈🐉🍦")
ic("------------------------")
ic("Vyper Examples Panel App")


# App Settings
ACCENT_COLOR = "#00286e"
SITE = "Vyper Example"
TITLE = "Simulations"

# Initialize Ledgers
distribution1 = Ledger()
distribution2 = Ledger()

# Beneficiary Account
beneficiary_account = Account(ledger=distribution1)
# ic(beneficiary_account)

# Bidding Account
bidding_account = Account(balance=10, ledger=distribution1)
# ic(bidding_account)

# Open Auction Parameters. Starting timestamp and number of seconds to run.
auction_start = dt.datetime.now() 
auction_start = auction_start.replace(second=0, microsecond=0, minute=0, hour=auction_start.hour)
auction_start = int(auction_start.timestamp())
bidding_time = 60*60
# ic(auction_start)
# ic(bidding_time)



# Initialize an Open Auction
open_auction = OpenAuction(
    beneficiary=beneficiary_account.address, 
    auction_start=auction_start,
    bidding_time=bidding_time,
    ledger=distribution1,
)

# ic(open_auction)
# ic(open_auction.param)

bid = Bid(
    value=5,
    timestamp= int(dt.datetime.now().timestamp()),
    sender = bidding_account.address,
    open_auction=open_auction,
)

withdraw = Withdraw(
    sender = bidding_account.address,
    open_auction=open_auction,
)

# Display The Model Examples App
models_row = pn.Row(
    beneficiary_account.view,
    open_auction.view,
    bid,
    withdraw,
)
models_pane = pn.Column(
    '# Models',
    models_row,
)

# Display The Simulation App 
simulation_pane = pn.Column(
    '# Simulation',
    Simulation(distributions=[distribution1, distribution2]).view,
)


# Serve The Panel App
def app():
    return pn.template.FastListTemplate(
        site=SITE,
        title=TITLE,
        header_background=ACCENT_COLOR,
        main=[
            simulation_pane,
            models_pane,
        ],
    ).servable()

app()#.show(threaded=True)
