__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

if (__name__ == "__main__"):
    import config
    import socket
    import select
    import sys

    address = (config.host, config.port)

    print("Starting connection to", address)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setblocking(False)
        server_socket.connect_ex(address)

        inputs = [sys.stdin, server_socket]

        while True:
            readable_io, _, _ = select.select(inputs, [], [])

            for io in readable_io:
                if (io == server_socket):
                    print(io.recv(4096))

                elif (io == sys.stdin):
                    message = sys.stdin.readline()

                    server_socket.send(message.encode("utf-8"))
                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()

