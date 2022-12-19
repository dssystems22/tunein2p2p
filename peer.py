import socket
import os
import shutil
import time

FORMAT = "utf-8"
SIZE = 1024

ADDR = ("127.0.0.1", 4000)


def main():
    print("Tune in to peer-to-peer!\nWhat's your port?")
    IP = socket.gethostname()
    PORT = int(input(">"))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Port saved!")

    if not (os.path.exists("peers")):
        os.mkdir("peers")

    if not (os.path.exists("peers" + "/" + str(PORT))):
        os.mkdir("peers" + "/" + str(PORT))

    while True:

        print("type \"help\" for help")
        cmd = input(">>>>>")
        match cmd:

            case 'center':
                client.connect(ADDR)
                client.send(f"{PORT}".encode(FORMAT))
                print(client.recv(SIZE).decode(FORMAT))
            # after center
            case 'listfiles':
                list_files = os.listdir("peers" + "/" + str(PORT))
                send_data = f"{cmd}@"
                send_data += ",".join(list_files)
                client.send(send_data.encode(FORMAT))
                print(client.recv(SIZE).decode(FORMAT))

            # after center
            case 'listpeers':
                client.send(cmd.encode(FORMAT))
                print(client.recv(SIZE).decode(FORMAT))
            # after center
            case 'check':
                print("Which file do you check:")
                file_name = input()
                send_data = f"{cmd}@{file_name}"
                client.send(send_data.encode(FORMAT))
                print(client.recv(SIZE).decode(FORMAT))
            case 'help':
                print("Available commands: quit, upl, downl, center")
            case 'quit':
                break
            case 'upl':
                client.bind((IP, PORT))
                client.listen(PORT)
                conn, addr = client.accept()
                print("connected", addr)
                filename = input("enter the file name: ")
                conn.send(filename.encode(FORMAT))
                with open("peers" + "/" + str(PORT) + "/" + filename, "rb") as f:
                    while True:
                        start = time.time()
                        bytes_read = f.read(SIZE)

                        if not bytes_read:
                            print("upload completed")
                            break
                        conn.sendall(bytes_read)

                        end = time.time()
                        if end - start > 0.2:
                            print("time out!")
                            break
                    conn.close()
            case 'downl':
                addresspeer = int(input("what is the peer's port :"))
                client.bind((IP, PORT))
                client.connect((IP, addresspeer))
                filename = client.recv(SIZE).decode(FORMAT)
                start = time.time()
                with open("peers" + "/" + str(PORT) + "/" + filename, "wb") as f:
                    while True:
                        bytes_read = client.recv(SIZE)
                        if not bytes_read:
                            print("download completed")
                            break
                        f.write(bytes_read)
                        end = time.time()
                        if end - start > 0.2:
                            print("Time out!")
                            break
            case _:
                print("No command found with name", cmd)
    #shutil.rmtree("peers/"+str(PORT))
    client.close()
    print("Disconnected")
if __name__ == "__main__":
    main()
