import sys, socket, select, Queue

from lib.Clients import *
from thread import *
from collections import deque

host = ''
services = [
    { 'name': 'dataService', 'port': 11211, 'client': dataClient },
    { 'name': 'monitoringService', 'port': 8000, 'client': monitoringClient }
]
sockets = {}

dataServicePort = 11211
monitoringPort = 8000

def main():

    # parse dbname from arguments
    if len(sys.argv) != 2:
        exit("Please provide a database name")

    dataConn = Data(sys.argv[1], True)

    for service in services:
        sockets[service['name']] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockets[service['name']].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sockets[service['name']].bind((host, service['port']))
        except socket.error as e:
            print(str(e))

        sockets[service['name']].listen(5)

    inputs = sockets.values()
    outputs = []
    message_queues = {}

    while inputs:

        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s in sockets.values():
                conn, addr = s.accept()
                conn.setblocking(0)
                inputs.append(conn)
                message_queues[conn] = Queue.Queue()
            else:
                data = s.recv(1024)
                print 
                if data:
                    incomingPort = s.getsockname()[1]

                    # Find the service in services dict
                    for service in services:
                        if service['port'] == incomingPort:
                            serv = service

                    clientRequest = serv['client'](data, dataConn)
                    message_queues[s].put(clientRequest)

                    # Add output channel for response
                    if s not in outputs:
                        outputs.append(s)

                else:
                    # Interpret empty result as closed connection
                    print('Closing connection')

                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

                    # Remove message queue
                    del message_queues[s]

        # Handle outputs
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Exception as e:
                # No messages waiting so stop checking
                # for writability.
                outputs.remove(s)
            else:
                print('Sending {!r} to {}'.format(next_msg, s.getpeername()))
                s.send(next_msg)
                s.shutdown(1)

        # Handle "exceptional conditions"
        for s in exceptional:
            # Stop listening for input on the connection
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

            # Remove message queue
            del message_queues[s]
        



    




if __name__ == "__main__":
    main()