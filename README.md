# wallet-iota-python
DONT USE THIS ON THE MAIN NET. It is still in the developing stage...

Test the wallet the docker testnet version using: https://github.com/daemonio/docker-iota-testnet

# Example of use

To SEND

     SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'

     # Let's create our connection.
     iota = MyIOTA('http://localhost:14265', SEED1)
     iota.enable_debug()
     iota.init_wallet()

     if iota.is_empty_wallet():
         iota.make_addr_list(start_index = 0, n = 5)

     print 'Your total fund is: ', iota.get_total_fund()
     
     transfer_value = 500
     dest_addr = Address('AXSJHWXGJMKMOS9LPZSATWDYRPTNVYAELDDWXMGTHOTLGWHRVDVZOBI9IQMELSEMMQKFVSNHYXYUWMZJBLRVJUPWEC')

     inputs, change_addr = iota.get_inputs(transfer_value, get_change_addr = True)
     output1 = iota.prepare_transfer(transfer_value, dest_addr, tag = 'TEST', msg = 'HELLO')

     iota.send_transfer(transfer_value, inputs, [output1], change_addr)

TO RECEIVE

     SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'

     # Let's create our connection.
     iota = MyIOTA('http://localhost:14265', SEED1)
     iota.enable_debug()
     iota.init_wallet()

     if iota.is_empty_wallet():
         iota.make_addr_list(start_index = 0, n = 5)

     print 'Your total fund is: ', iota.get_total_fund()
          
     txn_list = iota.find_transactions()
     
     for txn in iota.get_info_transactions(txn_list):
          addr_t, value_t, _, _ = txn

          print addr_t, value_t
