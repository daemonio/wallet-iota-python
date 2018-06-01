#!/usr/bin/env python2.7

from wallet import MyIOTA
import MAM
from iota import TryteString
import sys
import time
import subprocess
import os

from threading import Thread

#file_globals = runpy.run_path("file.py")

# wallet.py
# MAM.py

class Task:
    def __init__(self, id_t, total_t, ignore_addr = False):
        self.id_t = id_t
        self.total_t = total_t
        self.body = ['' for i in range(self.total_t)]
        self.mask = [False for i in range(self.total_t)]
        self.addr = ''
        self.filename = ''

        # Status flags
        self.saved_file = False
        self.executed = None

        # Output of the task
        self.output = []

        # addr is in the first position
        self.mask[0] = ignore_addr

    def _save_to_file(self):
        self.filename = 'task_'+self.addr[:10]+'.tsk'

        filefd = open(self.filename, 'w')

        for c in self.get_content():
            filefd.write(c)

        filefd.close()

        os.chmod(self.filename, 0765)
        pass


    def get_id(self):
        return self.id_t

    def get_len(self):
        return self.total_t

    def get_received(self):
        i = 0
        for m in self.mask:
            if m:
                i +=1

        return i

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr

    def is_executed(self):
        return self.executed == True

    def is_saved_file(self):
        return self.saved_file

    def set_executed(self, f = True):
        self.executed = f

    def set_saved_file(self):
        self.saved_file = True

    def set_msg_at_index(self, index_t, msg_t, overwrite = False):
        # if not to overwrite.. leave.
        if self.mask[index_t] and (not overwrite):
            print 'Not overwriting.'
            return None

        self.body[index_t] = msg_t
        self.mask[index_t] = True

    def is_content_left(self):
        for m in self.mask:
            if m == False:
                return True

        return False

    def get_content(self):
        return self.body

    def _execute(self, args):
        p = subprocess.Popen('./'+self.filename, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        # TODO: redirect to file
        
        #print "Command output : ", output
        #print "Command exit status/return code : ", p_status

        self.set_executed()
        self.output = output

    def execute(self):
        if self.is_content_left():
            return False

        if self.is_executed():
            return False

        if not self.is_saved_file():
            self._save_to_file()
            self.set_saved_file()

        # None (not executed) -> False (initiated) -> True (finalized)
        self.set_executed(False)

        thread = Thread(target = self._execute, args = [None])
        thread.start()
        thread.join()

class TaskList:
    def __init__(self):
        self.task_list = []

    def _get_info(self, tag):
        return map(int, tag.split('|'))

    def _get_task_with_id(self, id_t):
        for task in self.task_list:
            if task.get_id() == id_t:
                return task

        return None

    def show(self):
        for task in self.task_list:
            id_t = task.get_id()
            print 'Task: ', id_t
            print 'Executed: ', task.is_executed()

            if task.is_executed():
                print task.output
            #print 'Content:'
            #print 'Addr: |', task.get_addr()[:10], '|'
            #for c in task.get_content():
            #    print c
            #print '-------------------------------'

    def is_new_task(self, task):
        for t in self.task_list:
            if t.get_id() == task.get_id():
                return False

        return True

    def is_content_left(self, task):
        return task.is_content_left()

    def check_tag(self, tag):
        # True if we NEED to check the tangle
        id_t, index_t, total_t = self._get_info(tag)

        r = self._get_task_with_id(id_t)

        # New task
        if r == None:
            return True

        # Is there any content left?
        return r.is_content_left()

    def add_task(self, tag, msg):
        id_t, index_t, total_t = self._get_info(tag)
        id_t, index_t, total_t = int(id_t), int(index_t), int(total_t)

        # Create a task
        task = Task(id_t, total_t, ignore_addr = True)

        # Is it a new task?
        if self.is_new_task(task):
            if index_t == 0:
                task.set_addr(msg)
            else:
                task.set_msg_at_index(index_t, msg)

            self.task_list.append(task)
        else:
            # Update (if possible) existing task.
            task = self._get_task_with_id(id_t)
            if index_t == 0:
                task.set_addr(msg)
            else:
                task.set_msg_at_index(index_t, msg)

    def execute_tasks(self):
        for task in self.task_list:
            task.execute()

    def list_tasks(self):
        # There is a header.
        for task in self.task_list:
            id_t = task.get_id()

            print 'id_t: {0} | total: {1} received: {2}'.format(task.get_id(), \
                    task.get_len(), task.get_received())

def verify_tangle(iota, tasks):
    txn_list = iota.find_transactions()

    txn_all_msg = []

    # TODO: check value
    for txn in iota.get_info_transactions(txn_list):
        confirmed_t, addr_t, value_t, tag_t, msg_t = txn

        t = TryteString(tag_t)
        tag = t.decode()

        if tasks.check_tag(tag):
            m = TryteString(msg_t)
            msg = m.decode()

            tasks.add_task(tag, msg)
        else:
            print 'No new tasks...'

    #tasks.list_tasks()

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

while True:
    verify_tangle(iota, tasks)

    # Execute new tasks
    tasks.execute_tasks()

    time.sleep(10)

    tasks.show()
