from vyper_example.sim.account import Account


def test_account():
    account = Account()
    assert account.address
