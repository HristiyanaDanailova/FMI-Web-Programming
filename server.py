import socket
import requests
from bs4 import BeautifulSoup
import pickle


def extract(url):
   r = requests.get(url).text
   soup = BeautifulSoup(r,'html.parser')
   return soup.find_all('div', class_ = 'resultItem')

def transform(obj,offers_count):
    count = 0
    for item in obj:
        name_div = item.find('div', class_ = 'link')
        try:
            link = name_div.find('a')['href']
        except:
            link = 'Невалидна обява'
        name = name_div.find('a').text
        info_div = item.find('div', class_ = 'info')
        info = info_div.find('div').text.strip().replace('\n','').replace(' ','').replace('|',', ')
        try:
            comment = info_div.find('span').text
        except:
            comment = 'Липсва информация'
    
        price = item.find('div', class_ = 'price').text
        date = item.find('div', class_ = 'date').text
        count += 1
        if count <= offers_count:
            offer = {
             'model' : name,
             'price' : price,
             'info' : info,
             'comment' : comment,
             'date' : date,
             'link' : link
            }
            with open('db',mode='a+b') as file:
                pickle.dump(offer,file)
            
            f.write('Модел: ' + name + ', Цена: ' + price + ', Информация: ' + info + ', Коментар от търговеца: ' + comment + ', Дата: ' + date + ', Линк към обява: ' + link + '\n')
        else:
            return

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 6677

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen()

   
    while True:
        client, address = server.accept()
        print(f"Connection Established - {address[0]}:{address[1]}")

        file_path = 'db'
        try:
            fp = open(file_path,'r+').truncate(0)
        except IOError:
            fp = open(file_path, 'w+')
  

        offers_count = int(client.recv(1024))
        rem = offers_count % 19
        end_int = (offers_count - rem)//19 + 1

        f = open('cars.txt', "w", encoding='utf-8')
        f.write('Модел, Цена, Информация, Коментар от търговеца, Дата, Линк към обява\n')

        for x in range(1, end_int+1):
         if x == end_int:
            count = rem
         else :
            count = 19
         obj = extract(f'https://www.auto.bg/obiavi/avtomobili-dzhipove/page/{x}?searchres=wmuvtfv1&nup=013&sort=1')
         transform(obj,count)

        f.close()
        msg = 'Ready'
        client.send(msg.encode())

        client.close()
        
 
