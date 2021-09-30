__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

if (__name__ == "__main__"):
    import threading
    import config
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.bind((config.host, config.port))
        client_socket.listen(100)

        clients = []

        def spawn_client(client_connection, client_address):
            client_connection.send("Welcome to this chatroom!".encode("utf-8"))

            try:
                print("Waiting for data")
                data = client_connection.recv(4096)

                while data:
                    message = f"<{client_address[0]}> {data}"

                    print(message)
                    print("Propagating to clients")

                    for client in clients:
                        if client != client_connection:
                            try:
                                client.send(message.encode("utf-8"))

                            except:
                                client.close()

                                # if the link is broken, we remove the client
                                if client_connection in clients:
                                    clients.remove(client_connection)

                    print("Finished propagating")

                    print("Waiting for data")
                    data = client_connection.recv(4096)

                if client_connection in clients:
                    print("dead")
                    clients.remove(client_connection)

            except:
                return

        while True:
            connection, address = client_socket.accept()

            clients.append(connection)

            # prints the address of the user that just connected
            print(address[0] + " connected")
            threading.Thread(target=spawn_client, args=(connection, address)).start()
