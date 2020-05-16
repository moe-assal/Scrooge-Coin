from hashlib import sha256
from Crypto import validate_signature, sign, generate_keys

chain = []
TRANS_PER_BLOCK = 2
coins = []

sk, vk = generate_keys()
coins_pending_creation = []
trans_pending = []
coins_pending_deletion = []

Block = {
    "id": 0,
    "hash": sha256(bytes.fromhex("")).hexdigest(),
    "consumed coins": "",
    "transactions": [
        ["2.1", vk],
        ["1.3", vk],
        ["4.5", vk],
    ],
    "signatures": []
}
coins.append([])
for trans in Block['transactions']:
    Block['signatures'].append(sign(sk, trans.__str__()))
    coins[0].append(trans)
chain.append(Block)


def check_coin(coin, coin_id):
    global coins
    b, c = coin_id.split(" ")
    b, c = int(b), int(c)
    try:
        if coins[b][c] == coin:
            return True
        else:
            return False
    except IndexError:
        return False


def delete_coin(c_coin):
    """
    :param c_coin:
        [full_id, value, pk_from]
    :return:
    """
    global coins
    b, c = c_coin[0].split(" ")
    b, c = int(b), int(c)
    coins[b][c] = None


def create_coins(n_coins):
    global coins
    coins.append([])
    for coin in n_coins:
        coins[-1].append(coin[1:])


def create_block():
    global trans_pending, chain, coins_pending_deletion
    block = {
        "id": str(chain.__len__()),
        "hash": sha256(bytes(chain[-1].__str__(), encoding="ascii")).hexdigest(),
        "consumed": [],
        "transactions": [],
        "signatures": []
    }
    for coin, signature in trans_pending[:TRANS_PER_BLOCK]:
        block['transactions'].append(coin)
        block['signatures'].append(signature)
    create_coins(block['transactions'])
    for consumed_coin in coins_pending_deletion[:TRANS_PER_BLOCK]:
        block['consumed'].append(consumed_coin)
        delete_coin(consumed_coin)
    trans_pending = trans_pending[TRANS_PER_BLOCK:]
    coins_pending_deletion = coins_pending_deletion[TRANS_PER_BLOCK:]
    chain.append(block)


def receive_transaction(consumed_coin, coins_needed, signatures, fee):
    """
    :param fee:
        fee for each coin created
    :param pk_from:
    :param consumed_coin:
        [full_id, value, pk_from]
    :param coins_needed:
        [
            [value, pk_to], [value, pk_to]
        ]
    :param signatures:
    :var trans_pending:
        [
            [[coin_id, value, pk_to], signature]
        ]
    :return:
    """
    global coins_pending_deletion, trans_pending
    value = 0
    pk_from = consumed_coin[2]
    d = check_coin(consumed_coin[1:], consumed_coin[0])
    if d:
        for i, coin in enumerate(coins_needed):
            if validate_signature(pk_from, coin.__str__(), signatures[i]):
                value += float(coin[0])

            else:
                return False
        if value == float(consumed_coin[1]):
            for i, coin in enumerate(coins_needed):
                trans_pending.append([[str(trans_pending.__len__()), str(float(coin[0]) - fee), coin[1]], signatures[i]])
                coins_pending_deletion.append(consumed_coin)
        else:
            return False
    else:
        return False


if __name__ == '__main__':

    sk_client1, vk_client1 = generate_keys()
    receive_transaction(["0 1", "1.3", vk], [["0.9", vk_client1], ["0.2", vk], ["0.2", vk]], [
        sign(sk, ["0.9", vk_client1].__str__()),
        sign(sk, ["0.2", vk].__str__()),
        sign(sk, ["0.2", vk].__str__())
    ], 0.1)
    create_block()
    print(chain[1])
