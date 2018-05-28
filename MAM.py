from iota import TryteString

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

    def get_transactions_as_file_buffer(self, filename, value, bufsize, source_addr, dest_addr):
        txn_list = []
        index = 0

        buffer_msg = get_buffer_from_file(filename, bufsize)

        buffer_msg = ['{0}0'.format(dest_addr), buffer_msg]
        l = len(buffer_msg)

        for msg in buffer_msg:
            TAG = '{0}|{1}|{2}'.format(filename, index, l)
            TAG = TryteString.from_string(TAG)

            txn = iota.prepare_transfer(dest_addr, value, TAG, msg)
            txn_list.append(txn)

        return txn_list

