import os
import socket


IP = "0.0.0.0"
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
    conn.send(f"OK@ Tervetuola to File Server {name}".encode(FORMAT))
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        match cmd:
            case 'listpeers':
                send_data = "OK@"
                if len(DB.keys()) == 0:
                 send_data += "the sever doesnt have any peers"
                else:
                 send_data += "\n".join(val["name"] for val in DB.values())
                conn.send(send_data.encode(FORMAT))

            case 'listfiles':
                print("connected?")
                print(data)
                files = data[1].split(",")
                DB[addr]["files"] = files
                send_data = f"OK@Listed {len(files)} file(s)"
                conn.send(send_data.encode(FORMAT))
                

            case 'check':
                send_data = "OK@"
                file_name = data[1]
                print(data)
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
        handle_client(conn,addr)
        



if __name__ == "__main__":
    main()
