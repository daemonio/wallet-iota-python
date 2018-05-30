#!/usr/bin/env python2.7

from wallet import MyIOTA
import sys

from MAM import MAM

# wallet.py
# MAM.py

def send_file(iota, filename, source_addr, dest_addr):
    mam = MAM(iota)

    transfer_value = 0

    # These values really don't matter when transfer value = 0
    inputs, change_addr = iota.get_inputs(transfer_value)

    #output1 = iota.prepare_transfer(transfer_value, dest_addr, tag = 'TEST', msg = 'HELLO')
    outputs = mam.get_transactions_as_file_buffer(filename, 100, source_addr, dest_addr)

    iota.send_transfer(transfer_value, inputs, outputs, change_addr)

# Set your SEED.
SEED = 'G9OJZJEJFHFDRET9VBMSJEQEJSMPJHTSEZHYSXIFASRQFHDWMQHVGBSHHKIVXBTVDOLBYZCQJMFYEWTEB'

# Let's create our connection.
iota = MyIOTA('http://localhost:14265', SEED)

iota.enable_debug()

iota.init_wallet()

if iota.is_empty_wallet():
    iota.make_addr_list(start_index = 0, n = 10)

print 'Your total fund is: ', iota.get_total_fund()

# any addr for source addr
source_addr = iota.get_any_addr()

# dest addr
addr = 'UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD'
dest_addr = iota.Address(addr)

print 'Sending {0} to {1}...'.format(0, iota.s_addr(addr))
send_file(iota, '/etc/passwd', source_addr, dest_addr)
