from iota import TryteString
import random

# wallet.py

class MAM:
    def __init__(self, iota):
        self.iota = iota

    def get_buffer_from_file(self, filename, bufsize):
        f = open(filename, 'r')

        buf = []
        
        for line in f:
            line = line.rstrip('\n')

            i = 0
            while i < len(line):
                if bufsize < len(line):
                    j = bufsize
                else:
                    j = len(line)

                buf.append(line[i:i+j])

                i = i + j

        return buf
        f.close()

    def get_transactions_as_file_buffer(self, filename, bufsize, source_addr, dest_addr):
        txn_list = []
        index = 0
        value = 0

        header = ['{0}0'.format(source_addr)]
        body   = self.get_buffer_from_file(filename, bufsize)

        buffer_msg = []
        buffer_msg.extend(header)
        buffer_msg.extend(body)

        l = len(buffer_msg)

        for msg in buffer_msg:
            ID = random.randint(0, 1000)

            TAG = '{0}|{1}|{2}'.format(ID, index, l)
            TAG = TryteString.from_string(TAG)

            txn = self.iota.prepare_transfer(0, dest_addr, TAG, msg)
            txn_list.append(txn)

        return txn_list

    def save_transactions_buffer_as_file(self, txn_list, filename):
        pass

