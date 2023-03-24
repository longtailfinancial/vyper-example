import secrets
from eth_account import Account

def generate_eth_account():
    priv = secrets.token_hex(32)
    private = "0x" + priv
    public = Account.from_key(private).address

    return private, public

