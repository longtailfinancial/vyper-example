from ape import accounts, project

def test_account():
    account = accounts.test_accounts[0]
    return account

def test_deploy_open_auction():
    account = accounts.test_accounts[0]
    beneficiary = accounts.test_accounts[1]
    account.deploy(project.OpenAuction, beneficiary, 0, 1)

