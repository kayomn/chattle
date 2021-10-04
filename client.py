__author__ = "Kieran Osborne"
__version__ = "0.0.1"
__status__ = "Development"

if (__name__ == "__main__"):
    import asyncio
    import chattle
    import config
    import socket
    import sys

    username = input("username: ")
    address = (config.host, config.port)

    print("Starting connection to", address)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect_ex(address)
        print(server_socket.recv(config.message_max).decode("utf-8"))

        async def listen_server():
            response_data = server_socket.recv(config.message_max)

            while response_data:
                print(response_data.decode("utf-8"))

                response_data = server_socket.recv(config.message_max)

        # Listening for server responses has to be done on a separate unit of computation, such as an asynchronous
        # operation, so as not to block the console from working.
        asyncio.get_event_loop().create_task(listen_server())

        is_running = True

        while is_running:
            line = sys.stdin.readline().strip()

            if line:
                # Messages produced by this client are written to the terminal locally, rather than sending it to
                # server to then receive it back.
                if not line.startswith("/"):
                    sys.stdout.write("<You> ")
                    sys.stdout.write(line)
                    sys.stdout.write("\n")
                    sys.stdout.flush()

                server_socket.send(chattle.encode_message(username, line))

                if (line.lower() == "/quit"):
                    # Handle exiting on the client-side.
                    is_running = False

