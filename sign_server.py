import time
from multiprocessing.connection import Listener
import os
import threading

message_output_thread_count = 0
scrolling_active = True


# Clear the Console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Watch for incoming message while we are waiting
def sign_server_time(input_time):
    global message_output_thread_count
    local_thread_number = message_output_thread_count

    calculated_time = input_time / 0.1

    for a in range(int(calculated_time)):
        if local_thread_number != message_output_thread_count:
            return True
        time.sleep(0.1)

    return False


# Console Writing Function
def message_output(input_msg, input_scrolling_active):
    global message_output_thread_count
    local_thread_number = message_output_thread_count

    clear()
    des_message_input = input_msg.upper()

    des_message_output = ""
    full_console_output = ""
    sign_line_height = 7
    sign_line_max_disp_length = 128

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
            full_console_output += des_message_output[des_index] + " "

        full_console_output += "\n"

    # Limit console output to specified width
    temp_console_output = full_console_output.split('\n')
    message_length = len(temp_console_output[0])

    for z in range(2):

        proc_console_lines = []
        proc_console_output = ""

        # Trim initial message to sign width
        for y in range(sign_line_height):
            proc_console_lines.append(temp_console_output[y][0:sign_line_max_disp_length])
            proc_console_output += proc_console_lines[y] + "\n"
        print(proc_console_output)

        # Wait some time before cycling the message if longer than the screen length.
        # Exit if we get another message request
        if input_scrolling_active:
            if sign_server_time(2):
                return
        else:
            if sign_server_time(1):
                return

        # Check to see if message is longer than the width of the sign
        if message_length > sign_line_max_disp_length:
            #
            # Scrolling Mode
            #
            if input_scrolling_active:
                for x in range(message_length):
                    proc_console_lines = []
                    proc_console_output = ""

                    # Cycle through the message until all is seen
                    for y in range(sign_line_height):
                        proc_console_lines.append(temp_console_output[y][x:sign_line_max_disp_length + x])
                        proc_console_output += proc_console_lines[y] + "\n"

                        # Exit if we get another message request
                        if local_thread_number != message_output_thread_count:
                            return

                    clear()
                    time.sleep(0.1)
                    print(proc_console_output)
            #
            # Non Scrolling Mode
            #
            else:
                x = 0
                while x < message_length:
                    proc_console_lines = []
                    proc_console_output = ""

                    # Cycle through the message until all is seen
                    for y in range(sign_line_height):
                        proc_console_lines.append(temp_console_output[y][x:sign_line_max_disp_length + x])
                        proc_console_output += proc_console_lines[y] + "\n"

                    x += sign_line_max_disp_length
                    clear()
                    print(proc_console_output)

                    # Exit if we get another message request
                    if sign_server_time(2):
                        return


file = open("letters.txt", "r")

#
# Read in character mappings from text file
#
key = file.readline()
directory = []

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
# User Configuration
#
print("1 = default sign (7x128) no scroll\n"
      "2 = default sign (7x128) scroll\n" )

input_config = input("Choose your desired mode:")

if input_config == "1":
    scrolling_active = False
    print("1 = default sign (7x128) no scroll\n")
else:  # 2
    scrolling_active = True
    print("2 = default sign (7x128) scroll\n")


#
# Setup First Connection
#
address = ('localhost', 5000)
listener = Listener(address, authkey=b'1234')
conn = listener.accept()

#
# Main Loop, waiting for desired input from client
#
while True:

    try:
        msg = conn.recv()
    except:
        print("Error receiving message from client")

    message_output_thread = threading.Thread(target=message_output, args=(msg, scrolling_active,))

    # If we get the close command from client, close the connection and open a new listener
    if msg == 'close':
        conn.close()
        listener.close()

        address = ('localhost', 5000)
        listener = Listener(address, authkey=b'1234')
        conn = listener.accept()
    else:
        # Keep track of incoming messages so we know if console writing thread is getting out of sync
        message_output_thread_count += 1
        message_output_thread.start()
