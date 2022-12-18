import socket
import os
import shutil

FORMAT = "utf-8"
SIZE = 1024

ADDR=("0.0.0.0",4000)

def main():
    print("Tune in to peer-to-peer!\nWhat's your port?")
    IP = socket.gethostname()
    PORT = int(input(">"))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Port saved!")
   
    
    print("Choose your name:")
    peername = input()

      


  
    if not (os.path.exists(peername+"/"+str(PORT))):
        os.mkdir(peername+str(PORT))
    while True:
        
        print("type \"help\" for help")
        cmd = input(">>>>>")
        match cmd:

            case 'center':
                   
                    client.connect(ADDR)
                    client.send(f"{peername}".encode(FORMAT))
                    
                    print(client.recv(SIZE).decode(FORMAT))
                 
                 #list files
            case 'listfiles':

                    list_files = os.listdir(peername+str(PORT))
                    send_data = f"{cmd}@"
                    send_data += ",".join(list_files)
                    client.send(send_data.encode(FORMAT))

                    #check files
            case 'listpeers':
                 client.send(cmd.encode(FORMAT))
            case 'check':
                    print("Which file do you check:")
                    file_name = input()
                    send_data = f"{cmd}@{file_name}"
                    client.send(send_data.encode(FORMAT))
                   
            case 'help':
                print("Available commands: quit, displ, upl, downl, center")
            case 'quit':
                break
            case 'upl':
                client.bind((IP, PORT))
                client.listen(PORT)
                conn, addr = client.accept()
                print("connected", addr)
                filename = input("enter the file name: ")
                conn.send(filename.encode(FORMAT))
                with open(peername+str(PORT)+"/"+filename, "rb") as f:
                    while True:
                        bytes_read = f.read(SIZE)
                        if not bytes_read:
                            print("download fail")
                            break
                        conn.sendall(bytes_read)
                conn.close()
            case 'downl':
                addresspeer = int(input("what is the peer's port :"))
                client.bind((IP, PORT))
                client.connect((IP, addresspeer))
                
                filename = client.recv(SIZE).decode(FORMAT)
                with open(peername+str(PORT)+"/"+filename, "wb") as f:
                    while True:
                        bytes_read = client.recv(SIZE)
                        if not bytes_read:
                            print("upload fail")
                            break
                        f.write(bytes_read)
        
            case _:
                print("No command found with name", cmd)
    shutil.rmtree(peername+str(PORT))
   
    client.close()
    print("Disconnected")
if __name__ == "__main__":
    main()
