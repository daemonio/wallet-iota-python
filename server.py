#!/usr/bin/env python2.7

from wallet import MyIOTA
import MAM

from iota import TryteString

import sys

# wallet.py
# MAM.py

class Task:
    def __init__(self, filename):
        self.filefd = open(filename, 'r')
        self.start_time = 0
        self.end_time = 0
        pass

    def _execute(self):
        pass

    def execute(self):
        self.start_time = 0
        self._execute()
        self.end_time = 0

class Client:
    def __init__(self, addr):
        self.time = 0
        self.addr = addr
        self.task_id = None

    def get_addr(self):
        return self.addr

    def get_task_id(self):
        return self.task_id

    def set_time(self, time):
        self.time = time

    def set_task_id(self, task_id):
        self.task_id = task_id

    def get_time(self):
        return self.time

    def get_price(self):
        pass

class HandleClients:
    def __init__(self):
        self.client_list = []
        pass

    def add_client(self, client):
        self.client_list.append(client)

    def remove_client(self, client):
        pass

    def is_new_task(self, client):
        for c in self.cleint_list:
            if c.get_task_id() == client.get_task_id():
                return False

        return True

def verify_tangle(iota):
    txn_list = iota.find_transactions()

    for txn in iota.get_info_transactions(txn_list):
        confirmed_t, addr_t, value_t, tag_t, msg_t = txn
        t = TryteString(tag_t)
        print t.decode()
        pass

#
# This "server" can work without setting a SEED but as we're testing the wallet API,
# we will use one.
#

# Set your SEED.
SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'

# Let's create our connection to the node.
iota = MyIOTA('http://localhost:14265', SEED)
#iota.enable_debug()

iota.init_wallet()
iota.make_addr_list(start_index = 0, n = 1)

# Public address. The client should know this.
print iota.get_any_addr()

print 'Your total fund is: ', iota.get_total_fund()

verify_tangle(iota)

sys.exit()

# Infinite loop. Reading the tangle and creating tasks.
while True:
    pass

# TO RECEIVE
txn_list = iota.find_transactions()

for txn in iota.get_info_transactions(txn_list):
    confirmed_t, addr_t, value_t, tag_t, msg_t = txn

    #print '------', confirmed_t, addr_t, value_t

    print msg_t
