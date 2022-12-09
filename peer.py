import socket

FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Tune in to peer-to-peer!\nWhat's your port?")
    IP = socket.gethostbyname(socket.gethostname())
    PORT = int(input(">"))
    client.bind((IP, PORT))
    print("Port saved!")

    while True:
        print("type \"help\" for help")
        cmd = input(">")
        match cmd:
            case 'help':
                print("Available commands: quit, displ, upl")
            case 'quit':
                break
            case 'displ':
                # I don't get what was the function of this DISPLAY
                client.send(cmd.encode(FORMAT))
            case 'upl':
                client.listen(5)
                print("testi")
                # try:
                #     client.connect(ADDR)
                # except:
                #     # send_data = f"{cmd}@{filename}@{text}"
                #     # client.send(send_data.encode(FORMAT))
                #     print("some errors happen")
                # start sending
            case 'downl':
                port = input("Which port?")
                client.connect((IP, port))
                client_socket, address = client.accept()
                print(f"[+] {address} is connected.")
                # start receiving
            case _:
                print("No command found with name", cmd)

    client.close()
    print("Disconnected")

if __name__ == "__main__":
    main()
