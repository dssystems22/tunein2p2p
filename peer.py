import os
import socket
import shutil

IP = socket.gethostbyname(socket.gethostname())
PORT = 3000
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # Naming
    print("Choose your name:")
    name = input()
    os.mkdir(name)
    client.send(f"{name}".encode(FORMAT))

    while True:

        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "exit":
            print(f"server:{msg}")
            break
        elif cmd == 'OK':
            print(f"{msg}")

        data = input(">>>>> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "MORE":
            client.send(cmd.encode(FORMAT))

        elif cmd == "QUIT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "DISPLAY":
            client.send(cmd.encode(FORMAT))
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        elif cmd == "UPLOAD":

            path = data[1]
            with open(f"{path}", "r") as f:

                text = f.read()

            filename = path.split("/")[-1]
            try:
                send_data = f"{cmd}@{filename}@{text}"
                client.send(send_data.encode(FORMAT))
            except:
                print("some errors happen")

        elif cmd == "LIST_FILES":  # LIST_FILES
            list_files = os.listdir(name)
            send_data = f"{cmd}@"
            send_data += ",".join(list_files)
            client.send(send_data.encode(FORMAT))

        elif cmd == "CHECK":  # check
            print("Which file do you check:")
            file_name = input()
            send_data = f"{cmd}@{file_name}"
            client.send(send_data.encode(FORMAT))

        else:
            client.send(cmd.encode(FORMAT))

    print("Disconncted")
    shutil.rmtree(name)
    client.close()


if __name__ == "__main__":
    main()
