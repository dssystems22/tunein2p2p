import os
import socket
import threading

IP = "127.0.0.1"
PORT = 4000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DB = {}


def handle_client(conn, addr):
    name = conn.recv(SIZE).decode(FORMAT)
    print(f"Initialing Connection {name} with address {addr} connected.")
    DB[addr] = {
        "name": name,
        "files": []
    }
    conn.send(f"Tervetuola to File Server {name}".encode(FORMAT))
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        match cmd:
            case 'listpeers':
                send_data = ""
                if len(DB.keys()) == 0:
                    send_data += "the sever doesnt have any peers"
                else:
                    send_data += "\n".join(val["name"] for val in DB.values())
                conn.send(send_data.encode(FORMAT))

            case 'listfiles':
                files = data[1].split(",")
                DB[addr]["files"] = files
                send_data = f"Listed {len(files)} file(s)"
                conn.send(send_data.encode(FORMAT))

            case 'check':
                send_data = ""
                file_name = data[1]
                print(data)
                peer_found = []
                for peer in DB:
                    for file in DB[peer]["files"]:
                        if file == file_name:
                            peer_found.append(DB[peer]["name"]) 
                if peer_found:
                    send_data += f"Peer {peer_found} has the file {file_name}"
                else:
                    send_data += f"No one has file {file_name}"
                conn.send(send_data.encode(FORMAT))

            case 'quit':
                break

    print(f"Disconncted {addr}")
    DB.pop(addr)


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
        print(f"active connection {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
