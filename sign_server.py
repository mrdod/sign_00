from multiprocessing.connection import Listener
from os import system, name

# Clear the Console
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')



address = ('localhost', 5000)
listener = Listener(address, authkey=b'1234')
conn = listener.accept()

file = open("letters.txt", "r")

#
# Read in character mappings from text file
#
key = file.readline()
directory = [{"letter": "", "output": ""} ]

for index in key:
    output = ''

    while True:
        next_line = file.readline()

        # Account for multiple blank lines before Character
        while output == '' and next_line == '\n':
            next_line = file.readline()

        if next_line == '\n':
            break
        output += next_line

        if not next_line:
            break

    directory.append({"letter": index, "output": output})

file.close()


#
# Print Desired Text
#

while True:
    msg = conn.recv()

    if msg == 'close':
        conn.close()
        listener.close()

        address = ('localhost', 5000)
        listener = Listener(address, authkey=b'1234')
        conn = listener.accept()
    else:
        #clear()

        des_message_input = msg
        des_message_output = ""
        console_output = ""
        sign_line_height = 7

        # Look for each letter in the directory
        for y in des_message_input:
            for x in range(0, len(directory)):
                if directory[x].get("letter") == y:
                    des_message_output += directory[x].get("output")
                    des_message_output += "\n"

        des_message_output = des_message_output.split("\n")

        # Move letters from vertical orientation to horizontal
        for x in range(sign_line_height):
            for y in range(len(des_message_input)):
                des_index = x + (y * (sign_line_height + 1))
                console_output += des_message_output[des_index] + " "
            console_output += "\n"
        print(console_output)


print("Finshed!")
