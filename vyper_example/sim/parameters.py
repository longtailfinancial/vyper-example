import param as pm
import random

class Address(pm.String):
    """Ethereum Address Parameter"""

    def __init__(self, **params):
        # Empty string or eth address
        params['regex'] = '^$|^0x[a-fA-F0-9]{40}$'
        super(Address, self).__init__(**params)

    @staticmethod
    def random_address():
        return '0x' + ''.join(random.choice('0123456789abcdef') for n in range(40))

    @staticmethod
    def zero_address():
        return '0x' + '0' * 40


class Uint256(pm.Integer):
    """Unsigned 256 bit Integer Parameter"""
    def __init__(self, default=0, **params):
        super(Uint256, self).__init__(default=default, bounds=(0,(1<<256)-1), **params)

class Balance(Uint256):
    """Represents a token balance"""
    def __init__(self, **params):
        super(Balance, self).__init__(**params)

class Bool(pm.Boolean):
    """Unsigned 256 bit Integer Parameter"""
    def __init__(self, default=False, **params):
        super(Bool, self).__init__(default=default, **params)


