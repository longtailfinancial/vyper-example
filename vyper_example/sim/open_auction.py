import param as pm
import panel as pn
from vyper_example.sim.accounts import Account, Contract
import datetime as dt
from collections import defaultdict
from icecream import ic

class DefaultDict(defaultdict):
    __repr__ = dict.__repr__

class OpenAuction(Contract):

    beneficiary = pm.ClassSelector(class_=Account)

    # Auction Start and End
    auctionStart = pm.Date()
    auctionEnd = pm.Date()

    # Current state of the Auction
    highestBidder = pm.ClassSelector(class_=Account)
    highestBid = pm.Number(0, bounds=(0,None))

    # Set to true at the end. Dissalows any change
    ended = pm.Boolean()

    # Keep track of refunded bids so we can follow the withdraw pattern
    # public(HashMap[address, uint256])
    pendingReturns = pm.Dict(DefaultDict(lambda: 0)) 

    def __init__(self, beneficiary: Account, auction_start: int, bidding_time: int, **params):
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

    def end_auction(self, block):
        # Enforce Constraints
        assert block.timestamp >= int(self.auctionEnd.timestamp())
        assert not self.ended

        # Effects
        self.ended = True

        # Interactions
        self.send(self.beneficiary, self.highestBid)


    def view(self):
        return pn.Param(self.param, widgets={
            'auctionStart': pn.widgets.DatetimePicker,
            'auctionEnd': pn.widgets.DatetimePicker,
        })

class Transaction(pm.Parameterized):
    pass

class Withdraw(Transaction):
    sender = pm.ClassSelector(class_=Account)
    open_auction = pm.ClassSelector(class_=OpenAuction)
    withdraw = pm.Action(lambda self: self._withdraw())

    def _transaction(self):
        class MSG:
            sender = self.sender
        return [MSG()]

    def _withdraw(self):
        self.open_auction.withdraw(*self._transaction())

class Bid(Transaction):
    value = pm.Number(0, bounds=(0,None))
    timestamp = pm.Integer(bounds=(0,None))
    sender = pm.ClassSelector(class_=Account)
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
        try:
            self.open_auction.bid(*self._transaction())
            self.sender.send(self.open_auction, self.value)
        except AssertionError as e:
            ic("Transaction Failed")
            raise e

class EndAuction(Transaction):
    timestamp = pm.Integer(bounds=(0,None))
    open_auction = pm.ClassSelector(class_=OpenAuction)
    end_auction = pm.Action(lambda self: self._end_auction())

    def _transaction(self):
        class Block:
            timestamp = self.timestamp
        return [Block()]

    def _end_auction(self):
        self.open_auction.end_auction(*self._transaction())


