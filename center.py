import os
import socket
import threading

IP=socket.gethostbyname(socket.gethostname())
PORT=3000
ADDR=(IP,PORT)
SIZE=1024
FORMAT="utf-8"
SEVER_DATA_PATH="Testpath"


def handle_client(conn, addr):
     print(f"Initialing Conncection {addr} connected.")
     conn.send("OK@Tervetuola to File Server.".encode(FORMAT))

     while True:
          data=conn.recv(SIZE).decode(FORMAT)
          data=data.split("@")
          cmd=data[0]

          if cmd=='DISPLAY':
               files=os.listdir(SEVER_DATA_PATH)
               send_data="OK@"

               if len(files)==0:
                    send_data+="the sever doesnt contain files"
               else:
                    send_data+="\n".join(f for f in files)
               conn.send(send_data.encode(FORMAT))


          elif cmd=="UPLOAD":
               name,text = data[1], data[2]
               filepath=os.path.join(SEVER_DATA_PATH,name)
               with open(filepath,"w")as f:
                    f.write(text)
               
               send_data="OK@File Uploaded Successfully."
               conn.send(send_data.encode(FORMAT))

          elif cmd=="DELETE":
               files=os.listdir(SEVER_DATA_PATH)
               send_data="OK@"
               filename=data[1]

               if len(files)==0:
                    send_data+="none of files"
               else:
                    if filename in files:
                         os.remove(f"{SEVER_DATA_PATH}/{filename}")
                         send_data+="File Deleted"
                    else:
                         
                         send_data+="File Unavailable"

               conn.send(send_data.encode(FORMAT))

          elif cmd == "QUIT":
               break
          elif cmd=="MORE":
               data="OK@"
               data+="DISPLAY \n"
               data+="UPLOAD <Path>\n"
               data+="DELETE<filename>\n"
               data+="QUIT:Logout\n"
               data+="More: Tips"

               conn.send(data.encode(FORMAT))
     print(f"Disconncted {addr}")
     conn.close()


     
def main():
          print("Server is initiating")
          server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          server.bind(ADDR)
          server.listen()
          print(f"Server is listening {IP}:{PORT}")

          while True:
               conn,addr=server.accept()
               thread=threading.Thread(target=handle_client,args=(conn,addr))
               thread.start()
               print(f"active connection {threading.activeCount()-1}")

if __name__=="__main__":
     main()





               
               

               
