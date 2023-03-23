from ape import accounts, project

def test_counter():
    account = accounts.test_accounts[0]

    # Test Deploy
    contract = account.deploy(project.Counter)
    assert contract.counter() == 0

    # Test Increment
    contract.inc(sender=account)
    contract.inc(sender=account)
    assert contract.counter() == 2

    # Test Decrement
    contract.dec(sender=account)
    assert contract.counter() == 1

