# ShapeShift-API-Project
Check blockchain data against the ShapeShift API for transaction history

This repo is intended only to demonstrate my work product. The scripts will only work if modified with your own credentials.

`getTxData_BTC_RPC.py` will connect to your Bitcoin Core node to collect blockchain data and save to files.
`droplet.py` will load the txData, query the ShapeShift API, and upload results to a MongoDB.

`ShapeShift_sample_results.txt` contains a small sample of the 6 million+ transactions scraped from 2014-2021, from the following blockchains: 

`pprint(Counter(outgoingTypes))
Counter({'BTC': 1472575,
         'ETH': 992334,
         'LTC': 434582,
         'BCH': 366921,
         'DASH': 185616,
         'XRP': 175453,
         'DOGE': 155513,
         'EOS': 136261,
         'XMR': 111582,
         'ETC': 108311,
         'GNT': 100325,
         'OMG': 87907,
         'DGB': 85851,
         'SALT': 71094,
         'ZEC': 60892,
         'VTC': 56013,
         'BAT': 44810,
         'CVC': 44617,
         'RDD': 37965,
         'FUN': 36249,
         'REP': 28400,
         'ZRX': 25196,
         'ANT': 23279,
         'DCR': 21898,
         'DNT': 19382,
         'SNT': 12274,
         'POT': 9818,
         'BTG': 9634,
         'GNO': 9272,
         'BLK': 8996,
         'SC': 8680,
         'MONA': 7858,
         'QTUM': 7572,
         'ICN': 6543,
         'KMD': 6232,
         'EDG': 5783,
         'RLC': 5721,
         'BNT': 5515,
         'CLAM': 5371,
         'GAME': 4853,
         'PAY': 4827,
         'LBC': 4754,
         'WINGS': 4492,
         'DGD': 4192,
         'XEM': 4123,
         'WAVES': 4076,
         '1ST': 3883,
         'NXT': 3881,
         'GUP': 3645,
         'RCN': 2749,
         'TRST': 2724,
         'NEO': 2720,
         'NMR': 2475,
         'STORJ': 2463,
         'SNGLS': 2308,
         'MTL': 2018,
         'DAO': 1913,
         'BTS': 1476,
         'NMC': 1475,
         'FCT': 1370,
         'TUSD': 1333,
         'PPC': 1244,
         'SDC': 1164,
         'SWT': 1110,
         'MAID': 985,
         'POLY': 891,
         'VRC': 874,
         'USDT': 870,
         'START': 678,
         'TKN': 586,
         'BNB': 539,
         'USDC': 505,
         'MLN': 473,
         'VOX': 452,
         'DAI': 409,
         'LSK': 398,
         'NBT': 355,
         'STEEM': 331,
         'NVC': 300,
         'SJCX': 269,
         'MANA': 248,
         'ATOM': 221,
         'MKR': 210,
         'XCP': 196,
         'LINK': 114,
         'MINT': 113,
         'BCY': 104,
         'EMC': 103,
         'ZIL': 89,
         'FTC': 65,
         'PAX': 57,
         'BSV': 36,
         'BTCD': 34,
         'UNO': 33,
         'KNC': 31,
         'ARCH': 31,
         'HYPER': 31,
         'AE': 30,
         'MSC': 29,
         'PAXG': 18,
         'GEMZ': 17,
         'QRK': 12,
         'IFC': 12,
         'COMP': 10,
         'NEOS': 8,
         'FLO': 6,
         'STR': 3,
         'BAL': 2,
         'TRON': 2,
         'SHAPESHIFTCD': 2,
         'IXC': 1,
         'IOC': 1})`
