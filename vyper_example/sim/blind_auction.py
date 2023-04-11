import param as pm
import panel as pn
from vyper_example.sim.accounts import Account, Contract
from vyper_example.sim.parameters import Address
from web3 import Web3

class Event(pm.Parameterized):
    pass

class Bid(pm.Parameterized):
    blindedBid = pm.String()
    deposit = pm.Number(0, bounds=(0,None))

class AuctionEnded(Event):
    highestBidder = Address()
    highestBid = pm.Number(0, bounds=(0,None))

class OpenAuction(Contract):

    MAX_BIDS = 128

    # Auction parameters
    beneficiary = pm.ClassSelector(class_=Account)
    biddingEnd = pm.Date()
    revealEnd = pm.Date()

    # Set to true at the end. Dissalows any change
    ended = pm.Boolean()

    # Final auction state
    highestBid = pm.Number(0, bounds=(0,None))
    highestBidder = pm.ClassSelector(class_=Account)

    # State of the bids
    bids = pm.Dict(DefaultDict(lambda: []))
    bidCounts = pm.Dict(DefaultDict(lambda: 0))

    # Allowed withdrawals of previous bids
    pendingReturns = pm.Dict(DefaultDict(lambda: 0)) 


    def __init__(self, beneficiary: Account, bidding_time: int, reveal_time: int, block, **params):
        super().__init__(**params)
        self.beneficiary = beneficiary
        self.biddingEnd = block.timestamp + bidding_time
        self.revealEnd = self.biddingEnd + reveal_time


    def bid(self, blinded_bid, block, msg):
        # Check if bidding period is still open_auction
        assert block.timestamp < int(self.biddingEnd.timestamp())

        # Check that payer hasn't already placed maximum number of bids
        num_bids = self.bidCounts[msg.sender.address]
        assert numBids < self.MAX_BIDS

        self.bids[msg.sender.address][numBids] = Bid(
            blindedBid = blinded_bid,
            deposit = msg.value,
        )

        self.bidCounts[msg.sender.address] += 1

    # Returns True if bid placed successfully
    def place_bid(self, bidder: Account, value):
        # If bid is less than highest bid, bid fails
        if value <= self.highestBid:
            return False

        # Refund the previously highest bidder
        if self.highestBidder:
            self.pendingReturns[self.highestBidder.address] += self.highestBid

        # Place bid successfully and update auction state
        self.highestBid = value
        self.highestBidder = bidder

        return True


    # Reveal your blinded bids. You will get a refund for all correctly blinded
    # invalid bids and for all bids except for the totally highest.
    def reveal(self, num_bids, values, fakes, secrets, block, msg):
        # Check that the bidding period is over
        assert block.timestamp > self.biddingEnd

        # Check that reveal end has not passed
        assert block.timestamp < self.revealEnd

        # Check that the number of bids being revealed matches log for sender
        assert num_bids == self.bidCounts[msg.sender.address]

        # Calculate refund for sender
        refund = 0
        for i in range(self.MAX_BIDS):
            if i >= num_bids:
                break

            # Get bid to check
            bidToCheck: Bid = self.bids[msg.sender.address][i]

            # Check against encoded packet
            value = values[i]
            fake = fakes[i]
            secret = secrets[i]
            blindedBid = Web3.keccak(Web3.to_bytes(value) + Web3.to_bytes(fake) + secret)

            # If bid was not revealed, do not refund deposit
            assert blindedBid == bidToCheck.blindedBid

            # Add deposit to refund if bid was indeed revealed
            refund += bidToChekc.deposit
            if (not fake and bidToCheck.deposit >= value):
                if (self.place_bid(msg.sender.address, value)):
                    refund -=value

            # Make it impossible for the sender to re-claim the same deposit
            bidToCheck.blindedBid = None

            # Send refund if non-zero
            if refund:
                send(msg.sender.address, refund)







