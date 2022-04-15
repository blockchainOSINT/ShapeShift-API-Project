import time, json, os
from bitcoin_requests import BitcoinRPC
from collections import Counter

# rpc login & establish connection - set in bitcoin.conf file
username = '{username}'
password = '{password'
rpc = BitcoinRPC('http://127.0.0.1:8332', username, password)

# useful getblock keys: 'nextblockhash', 'nTx', 'tx', 'mediantime'

def getBlock(block_hash, block_height):
    """Scrape & save desired transaction data from a given block"""
    
    txData = []
    block = rpc.getblock(block_hash, 2)
    nextblockhash = block['nextblockhash']
    timestamp = block['time']
    if block['nTx'] > 1:
        for tx in block['tx']:
            txid = tx['txid']
            if 'vout' in tx:
                for vout in tx['vout']:
                    if 'addresses' in vout['scriptPubKey']:
                        for addr in vout['scriptPubKey']['addresses']:
                            if addr[0]=='1':
                                txData.append([addr, txid, block_height, timestamp])

    return txData, nextblockhash


def formatTxData(txData):
    """Format txData using heuritics to streamline process"""
    # disgard duplicates -- ShapeShift deposit addresses are only used once (>99.7% of test txs)
    # in tests, ~99.89% of btc txs have only one valid ShapeShift deposit addr per tx; filtering drastically redudes search time
    # txData = [address, txid, block_height, timestamp_unix]

    c_addrs = Counter([data[0] for data in txData])
    formatted_txData = [data for data in txData if c_addrs[data[0]]==1]
    c_txs = Counter([data[1] for data in formatted_txData])
    formatted_txData = [data for data in formatted_txData if c_txs[data[1]]<=2]

    return formatted_txData


def makeFiles(txData):
    """Write txData to files (30,000 transactions per file) for later use by droplet.py"""
    
    os.chdir(r"C:\Users\USER\btc_txData_legacy\new_data")

    save_num = 30000
    save_label = 0
    save_txData = []

    for index, data in enumerate(txData, start=1):
        save_txData.append(data)
        if index == save_num:
            save_label+=1
            with open(f'BTC_txData_{save_label:03d}.txt', 'w') as file:
                print(file.name)
                for data in save_txData:
                    file.write(json.dumps(data)+'\n')
            save_num += 30000
            save_txData = []
        elif len(txData) == index:
            save_label += 1
            with open(f'BTC_txData_{save_label:03d}.txt', 'w') as file:
                print(file.name)
                for data in save_txData:
                    file.write(json.dumps(data)+'\n')

def main():

    STARTBLOCK = 441075
    ENDBLOCK   = 487562
    start_time = time.time()
    all_txData = []
    nextblockhash = rpc.getblockhash(STARTBLOCK)
    print()

    for block_height in range(STARTBLOCK, ENDBLOCK+1):
        print(block_height)
        txData, nextblockhash = getBlock(nextblockhash, block_height)
        all_txData += txData

    all_txData = formatTxData(all_txData)
    makeFiles(all_txData)

    finish_time = time.time()
    time_elapsed = round((finish_time - start_time) / 60, 1)
    avg_speed = round((ENDBLOCK - STARTBLOCK) / time_elapsed * 60, 1)
    print("\nTotal Addresses Found:", len(all_txData), "\nTime Elapsed (mins):", time_elapsed, "\nAverage Speed:", avg_speed, "blocks per hour", "\n\a")

if __name__=="__main__":
    main()
