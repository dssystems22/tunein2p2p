import socket
import os

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
        cmd = input(">>>")
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
                conn,addr=client.accept()
                print("{}is connected",addr)
              
               
                filename="docker.txt"
                with open(filename, "rb") as f:
                    while True:
        # read the bytes from the file
                        bytes_read = f.read(SIZE)
                        if not bytes_read:
            # file transmitting is done
                            break
        # we use sendall to assure transimission in 
        # busy networks
                client.sendall(bytes_read)
# close the socket
                client.close()

                
                


           
              
                
                
              

            case 'downl':
                addresspeer = int(input("what is the peer's port :"))
                client.bind((IP, PORT))
                client.connect((IP, addresspeer))
                
                filename="docker.txt"
                with open(filename, "wb") as f:
                    while True:
        # read 1024 bytes from the socket (receive)
                        bytes_read = client.recv(SIZE)
                        if not bytes_read:    
            # nothing is received
            # file transmitting is done
                         break
        # write to the file the bytes we just received
                        f.write(bytes_read)

# close the client socket
                client.close()
# close the server socket
                client.close()
                
               
                

              






            case _:
                print("No command found with name", cmd)
    client.close()
    print("Disconnected")


if __name__ == "__main__":
    main()
