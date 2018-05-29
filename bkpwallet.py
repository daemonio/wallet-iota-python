#!/usr/bin/env python2.7

from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString, Transaction
import sys

import hashlib
import os.path
import random

class MyIOTA:
    def __init__(self, node, seed):
        self.node = node
        self.seed = seed
        self.api = False
        self._update = False
        self.transfers = []
        self._debug = False

        self.wallet = self.get_filename()

        self.addr_dict = {}

        self.min_weight_magnitude = 14

        self.api = Iota(self.node, self.seed)

        self.USED = True
        self.NOT_USED = False

    def Address(self, addr_string):
        return Address(addr_string)

    def get_addr_dict(self):
        return self.addr_dict

    def set_addr_dict(self, addr, value, used):
        self.addr_dict[addr] = (value, used)

    def s_addr(self, addr, n = 3):
        s_addr = str(addr)
        l = len(s_addr)

        return s_addr[:n]+'...'+s_addr[l-n:]

    def get_filename(self):
        h = hashlib.sha256()
        h.update(self.seed)
        filename = h.hexdigest()[:20]+'.txt'

        return filename

    def init_wallet(self):
        filename = self.wallet

        # file exists
        if os.path.isfile(filename):
            filefd = open(filename, 'r+')

            self.debug('Wallet file {0} exists. Opening it...'.format(filename))

            for line in filefd:
                line = line.rstrip('\n')

                addr, index, value, used = line.split(',')

                self.debug('reading from file: {0},{1},{2}'.format(self.s_addr(addr, 3), value, used))

                used = used == 'True'

                addr = Address(addr, key_index = int(index), security_level = 2)
                self.addr_dict[addr] = (int(index), int(value), used)

            filefd.close()
        else:
            filefd = open(filename, 'w')
            self.debug('Wallet file {0} doesnt exist. Creating it...'.format(filename))
            filefd.close()

    def is_empty_wallet(self):
        return len(self.addr_dict) == 0

    def get_fund_inputs(self, inputs):
        total_fund = 0

        for addr in inputs:
            index, value, used = self.addr_dict[addr]

            # TODO: abs. is this right?
            total_fund += abs(value)

        return total_fund

    def write_updates(self):
        filefd = open(self.wallet, 'w')

        self.debug('Writing (updating) wallet...')

        for addr in self.addr_dict:
            v = self.addr_dict[addr]

            line = 'Writing: {0},{1},{2},{3}\n'.format(self.s_addr(addr), v[0], v[1], v[2])
            self.debug(line)

            filefd.write('{0},{1},{2},{3}\n'.format(addr, v[0], v[1], v[2]))

        filefd.close()

    def update_wallet(self, input_fund, inputs, change_addr):
        copy_dict = self.addr_dict.copy()

        for addr in inputs:
            v = self.addr_dict[addr]
            #self.debug('Spending {0} from input {1}'.format(self.s_addr(addr), v))

            # Negative fund and used address
            new_value = (v[0], -v[1], not v[2])

            self.debug('Updating input address {0} to: {1}'.format(self.s_addr(addr), new_value))

            self.addr_dict[addr] = new_value

        change_fund = self.get_fund_inputs(inputs) - input_fund

        v = self.addr_dict[change_addr]
        change_value = (v[0], change_fund, self.NOT_USED)

        self.debug('Updating change address {0} to: {1}'.format(self.s_addr(change_addr), change_value))

        self.addr_dict[change_addr] = change_value

        self.write_updates()

    def enable_debug(self):
        self._debug = True

    def debug(self, msg):
        if self._debug:
            print '[+] Debug: ', msg

    def get_node_info(self):
        self.api.get_node_info()

    def make_addr_list(self, start_index, n):
        self.iota_assert(start_index >= 0 and n > 0, 'must be positive numbers. N should be at least 1.')

        result = self.api.get_new_addresses(index = start_index, count = n)
        addresses = result['addresses']

        for i in range(n):
            addr = addresses[i]
            value = self.get_addr_balance(addr)

            # TODO: Why always False
            self.addr_dict[addr] = (i, value, False)


        self.write_updates()

    def get_addr_balance(self, addr):
        # TODO: addr is a list with just one element
        result = self.api.get_balances([addr])

        balance = result['balances']

        return (balance[0])

    def prepare_transfer(self, transfer_value, dest_addr, tag = 'DEFAULT', msg = 'DEFAULT'):
        # TODO: verify address (checksum)
        # TODO: use mi, gi, etc

        msg = TryteString.from_string(msg)

        txn = ProposedTransaction(address=Address(dest_addr),
                message=msg,
                tag=Tag(tag),
                value=transfer_value,
                )

        return txn

    def find_transactions(self):
        addr_list = []
        for e in self.addr_dict.items():
            addr = e[0]

            addr_list.append(addr)

        return self.api.findTransactions(addresses = addr_list)['hashes']

    def get_bundle(self, trans):
        return self.api.getBundles(transaction = trans)

    def get_latest_inclusion(self, addrl):
        return self.api.get_latest_inclusion(hashes = addrl)

    def get_total_fund(self):
        total_fund = 0

        for addr in self.addr_dict.items():
            # key and value from dict
            k, v = addr

            index, value, used = v

            #if not used:
            total_fund += value

        return total_fund

    def send_transfer(self, input_fund, inputs, outputs, change_addr, savetofile = True):
        self.debug('Sending {0} transactions, please wait...'.format(len(outputs)))

        self.api.send_transfer(
                inputs=inputs,
                transfers=outputs,
                depth=7,
                change_address=change_addr,
                min_weight_magnitude=self.min_weight_magnitude)

        if savetofile:
            self.update_wallet(input_fund, inputs, change_addr)

    def get_trytes(self, hashl):
        return self.api.get_trytes(hashl)['trytes'][0]

    def get_transaction_from_trytes(self, trytes):
        txn = Transaction.from_tryte_string(trytes)

        return txn

    def get_transaction_fields(self, txn):
        #confirmed = str(txn.is_confirmed)
        timestamp = str(txn.timestamp)
        address   = str(txn.address)
        value     = str(txn.value)
        message   = str(txn.signature_message_fragment)
        #message   = str(txn.message)
        tag       = str(txn.tag)

        return (timestamp, address, value, tag, message)

    def get_info_transactions(self, transactions_hashes):
        txn_tuples = []

        for h in transactions_hashes:
            trytes = self.get_trytes([h])
            txn = self.get_transaction_from_trytes(trytes)

            # Get confirmed flag
            li_result = self.get_latest_inclusion([bytes(h)])
            confirmed_t = li_result['states'][h]

            (_, addr_t, value_t, tag_t, msg_t) = self.get_transaction_fields(txn)

            txn_tuples.append((confirmed_t, addr_t, value_t, tag_t, msg_t))

        return txn_tuples

    def get_any_addr(self):
        #TODO: verify
        #return self.addr_dict.keys()[0]
        k = self.addr_dict.keys()
        i = random.randint(0, len(k)-1)

        return k[i]

    def get_inputs(self, fund):
        # TODO: Zero fund
        fund_sum = 0
        addr_list = []
        change_addr = None

        # Zero fund transactions. We return any addr and any change_addr
        if fund == 0:
            addr_list.append(self.get_any_addr())
            change_addr = self.get_any_addr()

            return (addr_list, change_addr)

        for e in self.addr_dict.items():
            addr, v = e
            index, value, used = v

            if fund_sum < fund:
                #if value > 0 and not used:
                if value > 0 and used == self.NOT_USED:
                    fund_sum += value
                    self.debug('Found request: {0}. Found address {1} with fund {2}.'.format(fund, self.s_addr(addr), value))
                    addr_list.append(addr)

        for e in self.addr_dict.items():
            addr, v = e
            index, value, used = v

            if used == self.NOT_USED and addr not in addr_list:
                change_addr = addr

                self.debug('Using {0} as change addr.'.format(self.s_addr(addr)))
                break
        return (addr_list, change_addr)

        #else:
        #    # TODO
        #    self.iota_assert(True, 'No change addr available.')
    
    def iota_assert(self, condition, msg):
        if not condition:
            print 'Error: ', msg
            sys.exit(-1)
