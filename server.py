__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

if (__name__ == "__main__"):
    import config
    import traceback
    import socket as network
    import selectors
    import message

    class User:
        def __init__(self, user_socket: network.socket):
            self.socket = user_socket
            self.connection, self.address = user_socket.accept()
            self.selector = selectors.DefaultSelector()

            print("Accepted connection from", self.address)
            self.connection.setblocking(False)

        def close(self):
            self.selector.close()
            self.socket.close()

        def read(self):
            try:
                # Should be ready to read
                data = self.socket.recv(4096)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                if data:
                    print(message.deserialize(data))
                else:
                    raise RuntimeError("Peer closed.")

        def write(self):
            pass

        def run(self):
            try:
                while True:
                    events = self.selector.select(timeout=None)

                    for (key, mask) in events:
                        try:
                            if (mask & selectors.EVENT_READ):
                                self.read()

                            elif (mask & selectors.EVENT_WRITE):
                                self.write()

                        except Exception:
                            print(f"Exception raised on {self.address}: {traceback.format_exc()}"),
                            self.socket.close()

                    if not self.selector.get_map():
                        break

            except KeyboardInterrupt:
                print("caught keyboard interrupt, exiting")

            finally:
                self.selector.close()

    def init():
        address = (config.host, config.port)
        selector = selectors.DefaultSelector()

        with network.socket(network.AF_INET, network.SOCK_STREAM) as socket:
            # Avoid bind() exception: OSError: [Errno 48] Address already in use
            socket.setsockopt(network.SOL_SOCKET, network.SO_REUSEADDR, 1)
            socket.bind(address)
            socket.listen()

            print("Listening on", address)

            socket.setblocking(False)
            selector.register(socket, selectors.EVENT_READ, data=None)

            users = []

            try:
                while True:
                    events = selector.select(timeout=None)

                    for (key, mask) in events:
                        if key.data is None:
                            user = User(key.fileobj)

                            users.append(user)
                            user.run()

            except KeyboardInterrupt:
                print("Caught keyboard interrupt, exiting")

            finally:
                for user in users:
                    user.close()

                selector.close()

    init()
