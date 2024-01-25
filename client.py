import socket
import pickle

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 6677

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    num = input("Enter number in interval 0-1900: ")
    
    server.send(bytes(num, "utf-8"))
     
    msg = server.recv(1024).decode()
    while msg != 'Ready':
        msg = server.recv(1024)
    
    file = open('db','rb')
    try:
        while True:
            buffer = pickle.load(file)
            print('Модел: ' + buffer.get('model') + ', Цена: ' + buffer.get('price') + ', Информация: ' + buffer.get('info') + ', Коментар от търговеца: ' + buffer.get('comment') + ', Дата: ' + buffer.get('date') + ', Линк към обява: ' + buffer.get('link') + '\n')
    except EOFError:
         print('End of file')
    file.close()