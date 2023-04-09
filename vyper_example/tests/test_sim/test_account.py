from vyper_example.sim.accounts import Account
from vyper_example.sim.ledger import Ledger


def test_account():
    ledger = Ledger()
    account = Account(ledger=ledger)
    assert account.address
