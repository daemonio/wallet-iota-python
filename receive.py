#!/usr/bin/env python2.7

from wallet import MyIOTA

import MAM

# wallet.py
# MAM.py

# Set your SEED.
SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'

# Let's create our connection.
#iota = MyIOTA('http://localhost:14265', SEED)
iota = MyIOTA('http://150.164.7.219:14265', SEED)

iota.enable_debug()

iota.init_wallet()

# Get new addressess.
if iota.is_empty_wallet():
    iota.make_addr_list(start_index = 0, n = 10)

print 'Your total fund is: ', iota.get_total_fund()

iota.debug('Getting all transactions for the given addresses, please wait...')
txn_list = iota.find_transactions()

for txn in txn_list:
    b = iota.get_bundles(txn)['bundles']

    #t = b[0].group_transactions()[1]
    print len(b[0].group_transactions()[1])

    #print iota.get_info_transactions([t[0].hash])


#for txn in iota.get_info_transactions(txn_list):
#    confirmed_t, addr_t, value_t, tag_t, msg_t = txn
#
#    # Shows only the receveing address & its value.
#    print iota.s_addr(addr_t), value_t
