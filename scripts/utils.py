from ape import networks
import click

from ape.utils import ManagerAccessMixin

class Manager(ManagerAccessMixin):
    pass

def network():
    ecosystem_name = networks.provider.network.ecosystem.name
    network_name = networks.provider.network.name
    provider_name = networks.provider.name
    click.echo(f"You are connected to network '{ecosystem_name}:{network_name}:{provider_name}")

def block_height():
    manager = Manager()
    click.echo(f"Block height: {manager.chain_manager.blocks.height}")


def main():
    network()
    block_height()
