import param as pm
import panel as pn
from vyper_example.sim.parameters import Address
import datetime as dt
from collections import defaultdict


class OpenAuction(pm.Parameterized):

    beneficiary = Address()

    # Auction Start and End
    auctionStart = pm.Date()
    auctionEnd = pm.Date()

    # Current state of the Auction
    highestBidder = Address()
    highestBid = pm.Number(0, bounds=(0,None))

    # Set to true at the end. Dissalows any change
    ended = pm.Boolean()

    # Keep track of refunded bids so we can follow the withdraw pattern
    # public(HashMap[address, uint256])
    pendingReturns = pm.Dict(defaultdict(lambda: 0)) 

    def __init__(self, beneficiary, auction_start, bidding_time, **params):
        super(OpenAuction, self).__init__(**params)
        self.beneficiary = beneficiary
        self.auctionStart = dt.datetime.fromtimestamp(auction_start)
        self.auctionEnd = dt.datetime.fromtimestamp(auction_start+bidding_time)

    def bid(self, value, timestamp, sender, **kwargs):
        assert timestamp >= int(self.auctionStart.timestamp())
        assert timestamp < int(self.auctionEnd.timestamp())
        assert value > self.highestBid

        self.pendingReturns[self.highestBidder] += self.highestBid
        self.highestBidder = sender
        self.highestBid = value


    def view(self):
        return pn.Param(self.param, widgets={
            'auctionStart': pn.widgets.DatetimePicker,
            'auctionEnd': pn.widgets.DatetimePicker,
        })

class Bid(pm.Parameterized):
    value = pm.Number(0, bounds=(0,None))
    timestamp = pm.Integer(bounds=(0,None))
    sender = Address()
    open_auction = pm.ClassSelector(class_=OpenAuction)
    bid = pm.Action(lambda self: self._bid())

    # def values(self):
        # return {
            # 'value': self.value,
            # 'timestamp': self.timestamp,
            # 'open_acution': self.open_auction,
        # }

    def _bid(self):
        self.open_auction.bid(**self.param.values())



# class View(pm.Parameterized):
    # def display(self):
        # open_auction = OpenAuction(beneficiary=Address.random_address())
        # return pn.panel(open_auction)


