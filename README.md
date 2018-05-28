# wallet-iota-python
DONT USE THIS ON THE MAIN NET. It is still in the developing stage...

# Example of use

# Set your SEED.
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
