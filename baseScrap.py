from bs4 import BeautifulSoup
import time

with open('index.html','r') as htm_file:
    content = htm_file.read()
    # print(content)
    # time.sleep(3)

    soup = BeautifulSoup(content,'lxml')
    # print(soup.prettify())
    tags = soup.find('img') # only searching for the first tag matching
    tags2 = soup.find_all('img')
    # print(tags)
    # print('=============================================')
    # print(tags2)
    # divs = soup.find_all('div',class_='row') example with a filter on 
    # specific class. NB : the filter has a '_' it is class_ not class
    paragraphs = soup.find_all('p')
    i = 0
    for p in paragraphs:
        i+=1
        print(f"=========================== paragraph number{i}===================================" )
        print(p)
        print(f"============================paragraph text p{i}===================================" )
        print(p.text)
        


