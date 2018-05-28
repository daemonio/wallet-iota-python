#!/usr/bin/env python2.7

from wallet import MyIOTA
import sys

import MAM

# wallet.py

def send(iota, transfer_value, dest_addr):
    inputs, change_addr = iota.get_inputs(transfer_value)
    output1 = iota.prepare_transfer(transfer_value, dest_addr, tag = 'TEST', msg = 'HELLO')

    iota.send_transfer(transfer_value, inputs, [output1], change_addr)

# Set your SEED.
SEED = 'G9OJZJEJFHFDRET9VBMSJEQEJSMPJHTSEZHYSXIFASRQFHDWMQHVGBSHHKIVXBTVDOLBYZCQJMFYEWTEB'

# Let's create our connection.
iota = MyIOTA('http://localhost:14265', SEED)

iota.enable_debug()

iota.init_wallet()

if iota.is_empty_wallet():
    iota.make_addr_list(start_index = 0, n = 10)

print 'Your total fund is: ', iota.get_total_fund()

# value
transfer_value = 0

# source addr
source_addr = iota.get_addr_at_position(0)

# dest addr
addr = 'UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD'
dest_addr = iota.Address(addr)

print 'Sending {0} too {1}...'.format(transfer_value, iota.s_addr(addr))
send(iota, transfer_value, dest_addr)
