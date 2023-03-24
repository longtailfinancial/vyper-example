from ape import accounts, project
from ape.utils import ManagerAccessMixin
import click

class Manager(ManagerAccessMixin):
    pass

def simulate_open_auction(chain):
    account = accounts.test_accounts[0]
    beneficiary = accounts.test_accounts[1]
    tomorrow = chain.pending_timestamp + 24*60*60
    five_minutes = 5*60
    contract = account.deploy(project.OpenAuction, beneficiary, tomorrow, five_minutes)
    click.echo(f"Open Auction Deployed: {contract}")

def main():
    manager = Manager()
    simulate_open_auction(manager.chain_manager)

