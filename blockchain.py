from datetime import datetime


blockchain = []


def add_block(action, data):
    block = {
        "index": len(blockchain) + 1,
        "timestamp": str(datetime.now()),
        "action": action,
        "data": data,
        "previous_hash": blockchain[-1]["index"] if blockchain else 0
    }

    blockchain.append(block)
    return block

