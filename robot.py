#!/usr/bin/env python2.7

# Iissue 0-value transections JUST to approve others transaction.

from wallet import MyIOTA
import sys

# wallet.py

def send(iota, transfer_value, dest_addr):
    inputs, change_addr = iota.get_inputs(transfer_value)
    output1 = iota.prepare_transfer(transfer_value, dest_addr, tag = 'TEST', msg = 'HELLO')

    iota.send_transfer(transfer_value, inputs, [output1], change_addr)

# Set your SEED.
SEED   = 'WSHQRZICNFQUQPAPYWKFPWKTWWBPQNMTDNBYSGFZURGBWONDQEBPLNUXJVQTPYNFJKKTFATIVJTBSAWUX'

# Let's create our connection.
iota = MyIOTA('http://localhost:14265', SEED)

iota.enable_debug()

iota.init_wallet()

if iota.is_empty_wallet():
    iota.make_addr_list(start_index = 0, n = 10)

print 'Your total fund is: ', iota.get_total_fund()

transfer_value = 0

count = 0
while True:
    for addr in open('dest_addr_test_.log', 'r'):
        addr = addr.rstrip('\n')

        dest_addr = iota.Address(addr)

        print '[{0}] Sending {1} too {2}...'.format(count, transfer_value, iota.s_addr(addr))
        send(iota, transfer_value, dest_addr)
