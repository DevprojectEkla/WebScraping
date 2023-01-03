import os,sys
from bs4 import BeautifulSoup
from threading import Thread
import requests


def myprint(text):
    return print(text, flush=True)

key_word = input('enter a key-word or press enter:\n#>')
number_of_page = input('enter the number of page you want (80 images/page):\n#>')
number_of_page = int(number_of_page)
if key_word == '' or key_word == '\n':
    with open('list.txt','r') as f_keywordlist:
        key_word_list = f_keywordlist.read().splitlines()
else:
    key_word_list = [key_word]

if '+' in key_word:
    dirname = key_word.replace('+','-')
    filename = dirname
else:
    dirname = key_word
    filename = key_word

j = 0
pages_for_keyword = ('?','?')
summary = []
key_words_number = len(key_word_list)
for key_word in key_word_list:

    k = 0
    number_of_files = 0
    for n in range(1, number_of_page):
        
        links_for_download = []
        myreq_get = requests.get(f'https://www.wallpaperflare.com/search?wallpaper={key_word}&&page={n}') 
        if myreq_get.status_code == 404:
            print(f"No more page for this key word ({key_word}),\nseems like we've been throught all existing pages...")
            print(f"all images from key word {key_word} should have been dowloaded successfully.")
            print("done !")
            print(f'folder {dirname} has been successfully filled out. {j+1}/{key_words_number}')
            print(f'{key_words_number-j-1} remaining...')
            j += 1
            break
        else:
            html_text = myreq_get.text
        
            soup = BeautifulSoup(html_text, 'lxml')
            job = soup.find_all('a', {"itemprop": 'url'})
            if not os.path.isdir(f'img/{dirname}'):
                os.mkdir(f'img/{dirname}')
                print(f'folder {dirname} created')
            for link in job:
                # print(link.attrs["href"])
                link = link.attrs["href"] + "/download"    
                links_for_download.append(link)
# print(links_for_download)
            i = 0
            for link in links_for_download:
                url = requests.get(link).text
                soup = BeautifulSoup(url, 'lxml')
                job = soup.find_all(id = "show_img")
                for link in job:
                    url_img = link.attrs['src']
                    if not os.path.isfile(f'img/{dirname}/{filename}-{i}-page{n}.jpg'):
                        print(f"Downloading file from: {url_img}")
                        get_content = requests.get(url_img,stream=True)
                        with open(f'img/{dirname}/{filename}-page{n}-IMG{i}.jpg','wb') as fd:
                            for chunk in get_content.iter_content(chunk_size=512):
                                fd.write(chunk)
                            fd.close()
                        print(f"img file:{fd.name} copied\n {i}/{len(links_for_download)} : {len(links_for_download)-i} remaining")
                        print(f"page {n}/{number_of_page} : {number_of_page-n} remaining")
                    else:
                        print(f"the file img/{dirname}/{filename}-page{n}-{i}.jpg already exists.")
                        print(f"skipping this url...")
                i+=1
                number_of_files+=1
            print("===========================================================")
            print(f'Page {n} has been scrapped entirely in folder {dirname}.')
            print("===========================================================")
            print(f' still {number_of_page-n} to scrap remaining...')
            print("===========================================================")
            print(f'Scraping of page {n+1} started...')
            print("==================================")
            k+=1
    print("Done !")
    pages_for_keyword = key_word, f'{k} pages, {number_of_files} image files'
    summary.append(pages_for_keyword)
print('Job Terminated successfully.')
print('number of pages for each key word is :')
for item in summary:
     print(f"{item}")
print('Hope you enjoyed and Have fun with your new data !!!')
sys.exit(0)


def scrapping_iteration():
    pass


                




# for link in links_for_download:
#     url = requests.get(link)
#     soup = BeautifulSoup('url', 'lxml')
#     job = soup.find_all('img',{'id':'show_img'})
#     for link in job:
#         url_img = link.attrs['src']
#         print(url_img)


    




