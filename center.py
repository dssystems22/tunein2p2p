import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 3000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SEVER_DATA_PATH = "Testpath"
DB = {}


def handle_client(conn, addr):
    name = conn.recv(SIZE).decode(FORMAT)
    print(f"Initialing Connection {name} with address {addr} connected.")
    DB[addr] = {
        "name": name,
        "files": []
    }
    conn.send(f"OK@Tervetuola to File Server {name}".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == 'DISPLAY':
            files = os.listdir(SEVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "the sever doesnt contain files"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            print("test!")
            filepath = os.path.join(SEVER_DATA_PATH, name)
            with open(filepath, "w")as f:
                f.write(text)
            test=input()
            try:
                send_data = "OK@File Uploaded Successfully."
                conn.send(send_data.encode(FORMAT))
            except:
                print("The connection is lost")

        elif cmd == "DELETE":
            files = os.listdir(SEVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "none of files"
            else:
                if filename in files:
                    os.remove(f"{SEVER_DATA_PATH}/{filename}")
                    send_data += "File Deleted"
                else:

                    send_data += "File Unavailable"

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LIST_PEERS":
            send_data = "OK@"
            if len(DB.keys()) == 0:
                send_data += "the sever doesnt have any peers"
            else:
                send_data += "\n".join(val["name"] for val in DB.values())
            conn.send(send_data.encode(FORMAT))

        elif cmd == "LIST_FILES":
            files = data[1].split(",")
            DB[addr]["files"] = files
            send_data = f"OK@Listed {len(files)} file(s)"
            conn.send(send_data.encode(FORMAT))

        elif cmd == "CHECK":
            send_data = "OK@"
            file_name = data[1]
            peer_found = None
            for peer in DB:
                for file in DB[peer]["files"]:
                    if file == file_name:
                        peer_found = DB[peer]["name"]
            if peer_found:
                send_data += f"Peer {peer_found} has the file {file_name}"
            else:
                send_data += f"No one has file {file_name}"
            conn.send(send_data.encode(FORMAT))

        elif cmd == "QUIT":
            break
        elif cmd == "MORE":
            data = "OK@"
            data += "DISPLAY \n"
            data += "UPLOAD <Path>\n"
            data += "DELETE<filename>\n"
            data += "QUIT:Logout\n"
            data += "More: Tips"

            conn.send(data.encode(FORMAT))
    print(f"Disconncted {addr}")
    DB.pop(addr)
    conn.close()


def main():
    print("Server is initiating")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server is listening {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"active connection {threading.activeCount()-1}")


if __name__ == "__main__":
    main()
