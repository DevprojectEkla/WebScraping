import os
from bs4 import BeautifulSoup
import requests

with open('list.txt','r') as f_keywordlist:
    key_word_list = f_keywordlist.read().splitlines()

k = 0
for key_word in key_word_list:

    links_for_download = []
    html_text = requests.get(f'https://www.wallpaperflare.com/search?wallpaper={key_word}').text
    soup = BeautifulSoup(html_text, 'lxml')
    job = soup.find_all('a', {"itemprop": 'url'})
    os.mkdir(f'img/{key_word}')
    print(f'folder {key_word} created')
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
            print(f"Downloading file from: {url_img}")
            get_content = requests.get(url_img,stream=True)
            with open(f'img/{key_word}/{key_word}-{i}.jpg','wb') as fd:
                for chunk in get_content.iter_content(chunk_size=512):
                    fd.write(chunk)
                fd.close()
            print(f"img file:{fd.name} copied\n {i}/{len(links_for_download)} : {len(links_for_download)-i} remaining")
        i+=1
    print(f'folder {key_word} has been successfully filled out. {k+1}/len(key_word_list)')
    print(f'{len(key_word_list)-k-1} remaining...')
    k+=1
print("Done !")

            

                




# for link in links_for_download:
#     url = requests.get(link)
#     soup = BeautifulSoup('url', 'lxml')
#     job = soup.find_all('img',{'id':'show_img'})
#     for link in job:
#         url_img = link.attrs['src']
#         print(url_img)


    




