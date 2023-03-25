import param as pm
import panel as pn
from parameters import Address, Bool, Uint256


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


