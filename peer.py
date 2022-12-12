import socket

FORMAT = "utf-8"
SIZE = 2048


def main():

    print("Tune in to peer-to-peer!\nWhat's your port?")
    IP = socket.gethostname()
    PORT = int(input(">"))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Port saved!")

    while True:
        print("type \"help\" for help")
        cmd = input(">")
        match cmd:
            case 'help':
                print("Available commands: quit, displ, upl, downl")
            case 'quit':
                break
            case 'displ':
                print("comming soon")
            case 'upl':
                client.bind((IP, PORT))
                client.listen(PORT)
                connection, address = client.accept()
                print("Peers are connected")
            case 'downl':
                addresspeer = int(input("what is the peer's port :"))
                client.bind((IP, PORT))
                client.connect((IP, addresspeer))
            case _:
                print("No command found with name", cmd)
    client.close()
    print("Disconnected")


if __name__ == "__main__":
    main()
