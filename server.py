#!/usr/bin/env python2.7

from wallet import MyIOTA
import MAM

from iota import TryteString

import sys

# wallet.py
# MAM.py

class TaskList:
    def __init__(self):
        self.task_dict = {}
        pass

    def _get_info(self, tag):
        return tag.split('|')

    def _save_task_to_file(self, id_t):
        r = open(str(id_t) + '.py', 'w')

        first = True

        for l in self.task_dict[id_t]:
            if first:
                first = False
                continue

            r.write(l)

        r.close()

    def is_new_task(self, id_t):
        return id_t not in self.task_dict.keys()

    def is_new_index(self, id_t, index):
        return len(self.task_dict[id_t][index]) == 0

    def add_task(self, id_str, line_code):
        id_t, index_t, total_t = self._get_info(id_str)

        id_t, index_t, total_t = int(id_t), int(index_t), int(total_t)

        if self.is_new_task(id_t):
            body = ['' for i in range(total_t)]

            body[index_t] = line_code

            self.task_dict[id_t] = body
        else:
            #print 'index: ', index_t
            #print 'len do id: ', id_t, ' : ', len(self.task_dict[id_t])
            self.task_dict[id_t][index_t] = line_code

    def list_tasks(self):
        for id_t in self.task_dict:
            print 'id_t: {0} | msg length: {1}'.format(id_t, len(self.task_dict[id_t]))
            #self._save_task_to_file(id_t)

class Client:
    def __init__(self, addr):
        self.time = 0
        self.addr = addr
        self.task = None

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

def verify_tangle(iota, tasks):
    txn_list = iota.find_transactions()

    txn_all_msg = []

    for txn in iota.get_info_transactions(txn_list):
        confirmed_t, addr_t, value_t, tag_t, msg_t = txn
        t = TryteString(tag_t)
        m = TryteString(msg_t)

        tag = t.decode()
        msg = m.decode()

        tasks.add_task(tag, msg)
        pass

    tasks.list_tasks()

def is_task_exist(task_list, task):
    for t in task_list:
        if t.get_id() == task.get_id():
            return True

    return False

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

tasks = TaskList()
verify_tangle(iota, tasks)
