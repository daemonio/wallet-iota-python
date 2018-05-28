#!/usr/bin/env python2.7

from wallet import MyIOTA

# wallet.py

# Set your SEED.
SEED   = 'WSHQRZICNFQUQPAPYWKFPWKTWWBPQNMTDNBYSGFZURGBWONDQEBPLNUXJVQTPYNFJKKTFATIVJTBSAWUX'

# Let's create our connection.
iota = MyIOTA('http://localhost:14265', SEED)
iota.enable_debug()

iota.init_wallet()

if iota.is_empty_wallet():
    iota.make_addr_list(start_index = 0, n = 10)

print 'Your total fund is: ', iota.get_total_fund()

transfer_value = 900
dest_addr = iota.Address('UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD')

inputs, change_addr = iota.get_inputs(transfer_value, get_change_addr = True)
output1 = iota.prepare_transfer(transfer_value, dest_addr, tag = 'TEST', msg = 'HELLO')

iota.send_transfer(transfer_value, inputs, [output1], change_addr)
