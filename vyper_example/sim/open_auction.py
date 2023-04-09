import param as pm
import panel as pn
from vyper_example.sim.accounts import Account, Contract
from vyper_example.sim.parameters import Address
import datetime as dt
from collections import defaultdict
from icecream import ic

class OpenAuction(Contract):

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

    def __init__(self, beneficiary: Address, auction_start: int, bidding_time: int, **params):
        self.auctionStart = dt.datetime.fromtimestamp(auction_start)
        self.auctionEnd = dt.datetime.fromtimestamp(auction_start+bidding_time)
        super(OpenAuction, self).__init__(**params)
        self.beneficiary = beneficiary

    def bid(self, msg, block):
        # Enforce Constraints
        assert block.timestamp >= int(self.auctionStart.timestamp())
        assert block.timestamp < int(self.auctionEnd.timestamp())
        assert msg.value > self.highestBid

        # Refund the Previous Highest Bidder
        self.pendingReturns[self.highestBidder] += self.highestBid

        # Update the Highest Bidder and Bid
        self.highestBidder = msg.sender
        self.highestBid = msg.value

    def withdraw(self, msg):
        pending_amount = self.pendingReturns[msg.sender]
        self.pendingReturns[msg.sender] = 0
        self.send(msg.sender, pending_amount)



    def view(self):
        return pn.Param(self.param, widgets={
            'auctionStart': pn.widgets.DatetimePicker,
            'auctionEnd': pn.widgets.DatetimePicker,
        })

class Withdraw(pm.Parameterized):
    sender = Address()
    open_auction = pm.ClassSelector(class_=OpenAuction)
    withdraw = pm.Action(lambda self: self._withdraw())

    def _transaction(self):
        class MSG:
            sender = self.sender
        return [MSG()]

    def _withdraw(self):
        self.open_auction.withdraw(*self._transaction())

class Bid(pm.Parameterized):
    value = pm.Number(0, bounds=(0,None))
    timestamp = pm.Integer(bounds=(0,None))
    sender = Address()
    open_auction = pm.ClassSelector(class_=OpenAuction)
    bid = pm.Action(lambda self: self._bid())

    def _transaction(self):
        class MSG:
            value = self.value
            sender = self.sender
        class Block:
            timestamp = self.timestamp
        return MSG(), Block()

    def _bid(self):
        self.open_auction.bid(*self._transaction())
