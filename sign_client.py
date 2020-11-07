from multiprocessing.connection import Client

address = ('localhost', 5000)
conn = Client(address, authkey=b'1234')

val = input("Enter your value: ")

conn.send(val)
conn.send('close')
