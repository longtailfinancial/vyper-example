import panel as pn
import holoviews as hv
from vyper_example.sim.open_auction import OpenAuction, Bid, Withdraw, EndAuction
from vyper_example.sim.accounts import Account
from vyper_example.sim.ledger import Ledger
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
ledger = Ledger()

# Beneficiary Account
beneficiary_account = Account(ledger=ledger)

# Bidding Account
bidding_account = Account(balance=10, ledger=ledger)

# Open Auction Parameters. Starting timestamp and number of seconds to run.
auction_start = dt.datetime.now() 
auction_start = auction_start.replace(second=0, microsecond=0, minute=0, hour=auction_start.hour)
auction_start = int(auction_start.timestamp())
bidding_time = 60*60


# Initialize an Open Auction
open_auction = OpenAuction(
    beneficiary=beneficiary_account, 
    auction_start=auction_start,
    bidding_time=bidding_time,
    ledger=ledger,
)

bid = Bid(
    value=2,
    timestamp= int(dt.datetime.now().timestamp()),
    sender = bidding_account,
    open_auction=open_auction,
)

withdraw = Withdraw(
    sender = bidding_account,
    open_auction=open_auction,
)

end_auction = EndAuction(
    timestamp= auction_start+bidding_time+1,
    open_auction=open_auction,
)

# Display The Model Examples App
open_auction_row = pn.Row(
    pn.Column(
        beneficiary_account.view,
        bidding_account.view,
    ),
    open_auction.view,
    bid,
    withdraw,
    end_auction,
)
models_pane = pn.Column(
    '# Open Auction Model',
    open_auction_row,
)

# Display The Simulation App 
ledger_pane = pn.Column(
    '# Simulation Ledger',
    ledger.view,
)


# Serve The Panel App
def app():
    return pn.template.FastListTemplate(
        site=SITE,
        title=TITLE,
        header_background=ACCENT_COLOR,
        main=[
            ledger_pane,
            models_pane,
        ],
    ).servable()

app()#.show(threaded=True)
