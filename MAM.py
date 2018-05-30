from iota import TryteString
import random

# wallet.py

class MAM:
    def __init__(self, iota):
        self.iota = iota

    def get_buffer_from_file2(self, filename, bufsize):
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



    def get_buffer_from_file(self, filename, bufsize):
        r = open(filename, 'r')

        buf = ['']
        currentIndex   = 0
        currentLength  = 0

        for l in r.readlines():
            endLoop = False

            while not endLoop:
                # currentIndex needs more chars.
                if len(buf[currentIndex]) < bufsize:
                    currentLength = len(buf[currentIndex])

                    # how many chars left.
                    left = bufsize - currentLength

                    # put the remaining for the line and go to
                    # get the next one.
                    if len(l) < left:
                        endLoop = True

                        buf[currentIndex] += l
                    else:
                        # line still has more than bufsize chars.
                        # save them and update the line.
                        l2 = l[:bufsize]

                        buf[currentIndex] += l2

                        l = l[bufsize:]
                else:
                    # when currentIndex is full. Just create a new
                    # position in the buf.
                    currentIndex += 1
                    buf.append('')

        r.close()

        return buf

    def get_transactions_as_file_buffer(self, filename, bufsize, ID_msg, source_addr, dest_addr):
        txn_list = []
        index = 0
        value = 0

        header = ['{0}'.format(source_addr)]
        body   = self.get_buffer_from_file(filename, bufsize)

        buffer_msg = []
        buffer_msg.extend(header)
        buffer_msg.extend(body)

        l = len(buffer_msg)

        for msg in buffer_msg:
            TAG = '{0}|{1}|{2}'.format(ID_msg, index, l)
            TAG = TryteString.from_string(TAG)

            txn = self.iota.prepare_transfer(0, dest_addr, TAG, msg)
            txn_list.append(txn)

            index += 1

        return txn_list

    def save_transactions_buffer_as_file(self, txn_list, filename):
        pass

