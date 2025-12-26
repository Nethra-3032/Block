wallets = {}


def create_wallet(address):
    if address not in wallets:
        wallets[address] = 10000  # initial tokens


def transfer(sender, receiver, amount):
    create_wallet(sender)
    create_wallet(receiver)

    if wallets[sender] >= amount:
        wallets[sender] -= amount
        wallets[receiver] += amount
        return True

    return False


def get_wallets():
    return wallets
