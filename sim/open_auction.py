import param as pm
import panel as pn
from web3 import Web3
import random


class Address(pm.String):
    """Ethereum Address Parameter"""

    def __init__(self, **params):
        # Empty string or eth address
        params['regex'] = '^$|^0x[a-fA-F0-9]{40}$'
        super(Address, self).__init__(**params)

    # def _validate_value(self, val, allow_None):
        # super(Address, self)._validate_value(val, allow_None)
        # if not Web3.isAddress(val):
            # raise ValueError("Address parameter %r must be a valid ethereum address, not %r." % (self.name, val))

    @staticmethod
    def random_address():
        return '0x' + ''.join(random.choice('0123456789abcdef') for n in range(40))

    @staticmethod
    def zero_address():
        return '0x' + '0' * 40


class Uint256(pm.Integer):
    """Unsigned 256 bit Integer Parameter"""
    def __init__(self, default=0, softbounds=None, **params):
        super(Uint256, self).__init__(default=default, bounds=(0,(1<<256)-1), softbounds=softbounds, **params)


class Bool(pm.Boolean):
    """Unsigned 256 bit Integer Parameter"""
    def __init__(self, default=False, **params):
        super(Bool, self).__init__(default=default, **params)


class OpenAuction(pm.Parameterized):

    beneficiary = Address()

    # Auction Start and End
    auctionStart = Uint256()
    auctionEnd = Uint256()

    # Current state of the Auction
    highestBidder = Address()
    highestBid = Uint256()

    # Set to true at the end. Dissalows any change
    ended = Bool()

    # Keep track of refunded bids so we can follow the withdraw pattern
    # public(HashMap[address, uint256])
    pendingReturns = pm.Dict(default={}) 




class View(pm.Parameterized):
    def display(self):
        open_auction = OpenAuction(beneficiary=Address.random_address())
        return pn.panel(open_auction)


