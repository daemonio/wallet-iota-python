#!/usr/bin/env python2.7

from wallet import MyIOTA

# wallet.py

# Set your SEED.
SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'

# Let's create our connection.
iota = MyIOTA('http://localhost:14265', SEED)
iota.enable_debug()

iota.init_wallet()

if iota.is_empty_wallet():
    iota.make_addr_list(start_index = 0, n = 5)

print 'Your total fund is: ', iota.get_total_fund()

# TO RECEIVE
txn_list = iota.find_transactions()
for txn in iota.get_info_transactions(txn_list):
    addr_t, value_t, _, _ = txn

    print addr_t, value_t
