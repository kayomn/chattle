__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

if (__name__ == "__main__"):
    import config
    import socket as network
    import message

    def init() -> None:
        address = (config.host, config.port)

        print("Starting connection to", address)

        with network.socket(network.AF_INET, network.SOCK_STREAM) as socket:
            socket.setblocking(False)
            socket.connect_ex(address)

            while True:
                message_body = input("Enter a message: ")

                print("\n")
                socket.send(message.serialize("Kayomn", message_body))

    init()

