from ape import accounts, project

def test_deploy_open_auction(chain):
    account = accounts.test_accounts[0]
    beneficiary = accounts.test_accounts[1]
    tomorrow = chain.pending_timestamp + 24*60*60
    five_minutes = 5*60

    account.deploy(project.OpenAuction, beneficiary, tomorrow, five_minutes)

