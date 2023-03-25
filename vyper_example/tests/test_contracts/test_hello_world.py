from ape import accounts, project

def test_deploy_hello_world():
    account = accounts.test_accounts[0]
    contract = account.deploy(project.HelloWorld)
    assert contract.greet() == 'Hello World!'

