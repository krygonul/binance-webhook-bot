def has_open_position(client, symbol):
    positions = client.get_account()["balances"]
    for pos in positions:
        if pos["asset"] in symbol and float(pos["free"]) > 0:
            return True
    return False