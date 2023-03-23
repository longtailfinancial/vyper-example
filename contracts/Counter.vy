# @version >=0.3.8

counter: public(uint128)

@external
def __init__():
    self.counter = 0

@external
def inc():
    self.counter += 1

@external
def dec():
    self.counter -= 1

