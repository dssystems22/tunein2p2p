import socket
import os

FORMAT = "utf-8"
SIZE = 2048
SEPARATOR = "S"


def main():
    print("Tune in to peer-to-peer!\nWhat's your port?")
    IP = socket.gethostname()
    PORT = int(input(">"))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Port saved!")
    if not (os.path.exists("peers")):
        os.mkdir("peers")
    if not (os.path.exists("peers/"+str(PORT))):
        os.mkdir("peers/"+str(PORT))
    while True:
        print("type \"help\" for help")
        cmd = input(">>>")
        match cmd:
            case 'help':
                print("Available commands: quit, displ, upl, downl")
            case 'quit':
                break
            case 'upl':
                client.bind((IP, PORT))
                client.listen(PORT)
                conn, addr = client.accept()
                print("connected", addr)
                filename = input("enter the file name: ")
                conn.send(filename.encode(FORMAT))
                with open("peers/"+str(PORT)+"/"+filename, "rb") as f:
                    while True:
                        bytes_read = f.read(SIZE)
                        if not bytes_read:
                            break
                        conn.sendall(bytes_read)
                conn.close()
            case 'downl':
                addresspeer = int(input("what is the peer's port :"))
                client.bind((IP, PORT))
                client.connect((IP, addresspeer))
                filename = client.recv(SIZE).decode(FORMAT)
                with open("peers/"+str(PORT)+"/"+filename, "wb") as f:
                    while True:
                        bytes_read = client.recv(SIZE)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                        print(f)
            case _:
                print("No command found with name", cmd)
    client.close()
    print("Disconnected")
if __name__ == "__main__":
    main()
