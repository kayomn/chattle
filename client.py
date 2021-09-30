__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

if (__name__ == "__main__"):
    import chattle
    import config
    import socket
    import select
    import sys

    username = input("username: ")
    address = (config.host, config.port)

    print("Starting connection to", address)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setblocking(False)
        server_socket.connect_ex(address)

        # Input may be written by the user or received from the server. Both cases have to be handled.
        inputs = [sys.stdin, server_socket]

        while True:
            # Listen for input.
            readable_io, _, _ = select.select(inputs, [], [])

            for io in readable_io:
                if (io == server_socket):
                    response_data = io.recv(config.message_max)

                    if not response_data:
                        exit(0)

                    print(response_data.decode("utf-8"))

                elif (io == sys.stdin):
                    # Messages produced by this client are written to the terminal locally, rather than sending it to
                    # server to then receive it back.
                    line = sys.stdin.readline()

                    if not line.startswith("/"):
                        sys.stdout.write("<You> ")
                        sys.stdout.write(line)
                        sys.stdout.flush()

                    server_socket.send(chattle.encode_message(username, line))

