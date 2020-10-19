from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(20)
print('the boat is ready to recieve')

while True:
    connectionSocket, addr =  serverSocket.accept()
    #接收到客户端传来的信息
    information = connectionSocket.recv(1024).decode()
    #对接收到的信息进行解析
    info_split = information.split('*')
    boat_num = info_split[0]
    action = info_split[1]
    print('接收到信息：',boat_num, action)
    #组装预测结果信息
    info_back = str(boat_num)+'*'+'1-ok'
    print('返回信息：',info_back)
    connectionSocket.send(info_back.encode())
    connectionSocket.close()
