#!/usr/bin/env python2.7

from wallet import MyIOTA
import sys
import random

from MAM import MAM

# wallet.py
# MAM.py

def send_file(iota, filename, source_addr, dest_addr):
    mam = MAM(iota)

    transfer_value = 0

    # These values really don't matter when transfer value = 0
    inputs, change_addr = iota.get_inputs(transfer_value)

    ID_msg = random.randint(0, 1000)

    #output1 = iota.prepare_transfer(transfer_value, dest_addr, tag = 'TEST', msg = 'HELLO')
    outputs = mam.get_transactions_as_file_buffer(filename, 500, ID_msg, source_addr, dest_addr)

    iota.send_transfer(transfer_value, inputs, outputs, change_addr)

# Set your SEED.
SEED = 'G9OJZJEJFHFDRET9VBMSJEQEJSMPJHTSEZHYSXIFASRQFHDWMQHVGBSHHKIVXBTVDOLBYZCQJMFYEWTEB'

# Let's create our connection.
iota = MyIOTA('http://localhost:14265', SEED)
iota.enable_debug()

# Test of node is up.
#print iota.get_node_info()

# Create wallet file.
iota.init_wallet()

# Get new addressess.
if iota.is_empty_wallet():
    iota.make_addr_list(start_index = 0, n = 10)

print 'Your total fund is: ', iota.get_total_fund()

# any addr for source addr
source_addr = iota.get_any_valid_addr()

# dest addr
addr = 'UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD'
dest_addr = iota.Address(addr)

# value to transfer
transfer_value = 100

# inputs & change address (entrada e troco)
inputs, change_addr = iota.get_inputs(transfer_value)

# output (the transaction where the IOTA is going to)
output1 = iota.prepare_transfer(transfer_value, dest_addr, 'TAG', 'WHATEVER')

iota.debug('Sending transaction.. please wait.')

# Send our transaction
iota.send_transfer(transfer_value, inputs, [output1], change_addr)
