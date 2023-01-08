import os,sys
from bs4 import BeautifulSoup
from threading import Thread
import requests
from progressbar import printProgressBar


def myprint(text):
    return print(text, flush=True)

# key_word = input('enter a key-word or press enter:\n#>')
# number_of_page = input('enter the number of page you want (80 images/page):\n#>')
# number_of_page = int(number_of_page)

class Algo_G():
    

    def __init__(self):

        self._KILL = False 
        

    @staticmethod
    def define_key_word_entry(key_word):
        '''check if a key word is read from the input field or if a file lsit of key words should be used instead '''
        
        if os.path.isfile(key_word):
            with open(key_word,'r') as f_keywordlist:
                key_word_list = f_keywordlist.read().splitlines()
        else:
            key_word_list = [key_word]

        return key_word_list

    def main_iteration(self, key_word_list, number_of_page):
        j = 0
        pages_for_keyword = ('?','?')
        summary = []
        key_words_number = len(key_word_list)
        printProgressBar(0, key_words_number, prefix='Keywords progress', suffix= 'keyword list complete', length=50)
        for key_word in key_word_list:
            dirname = key_word
            filename = dirname
            if '+' in key_word:
                dirname = key_word.replace('+','-')
                filename = dirname
            if ' ' in key_word:
                dirname = key_word.replace(' ','-')
                filename = dirname
                key_word = key_word.replace(' ','+')
            if self._KILL:
                break
            k = 0
            printProgressBar(0, number_of_page, prefix='Downloading page in progress', suffix= 'all page complete', length=50)
            number_of_files = 0
            for n in range(1, number_of_page):
                if self._KILL:
                    break
                links_for_download = []
                myreq_get = requests.get(f'https://www.wallpaperflare.com/search?wallpaper={key_word}&&page={n}') 
                if myreq_get.status_code == 404:
                    myprint(f"No more page for this key word ({key_word}),\nseems like we've been throught all existing pages...")
                    myprint(f"all images from key word {key_word} should have been dowloaded successfully.")
                    myprint("done !")
                    myprint(f'folder {dirname} has been successfully filled out. {j+1}/{key_words_number}')
                    myprint(f'{key_words_number-j-1} remaining...')
                    j += 1
                    printProgressBar(j, key_words_number,prefix='Keywords progress', suffix= 'keyword list complete', length=50)
                    break
                else:
                    html_text = myreq_get.text
                
                    soup = BeautifulSoup(html_text, 'lxml')
                    job = soup.find_all('a', {"itemprop": 'url'})
                    if not os.path.isdir(f'img/{dirname}'):
                        os.mkdir(f'img/{dirname}')
                        myprint(f'folder {dirname} created')
                    for link in job:
                        if self._KILL:
                            break
                        # myprint(link.attrs["href"])
                        link = link.attrs["href"] + "/download"    
                        links_for_download.append(link)
# myprint(links_for_download)
                    i = 0
                    printProgressBar(0, len(links_for_download), prefix='Downloading Files in progress', suffix= 'Files Complete', length=50)

                    for link in links_for_download:
                        if self._KILL:
                            break
                        url = requests.get(link).text
                        soup = BeautifulSoup(url, 'lxml')
                        job = soup.find_all(id = "show_img")
                        for link in job:
                            if self._KILL:
                                break
                            url_img = link.attrs['src']
                            if not os.path.isfile(f'img/{dirname}/{filename}-{i}-page{n}.jpg'):
                                print(f"Downloading file from: {url_img}")
                                get_content = requests.get(url_img,stream=True)
                                size = get_content.headers['Content-length']
                                with open(f'img/{dirname}/{filename}-page{n}-IMG{i}.jpg','wb') as fd:

                                    printProgressBar(0, len(links_for_download), prefix=f'Downloading file in progress', suffix= 'file download Complete', length=10, fill='x')
                                    f = 0
                                    for chunk in get_content.iter_content(chunk_size=512):
                                        if self._KILL:
                                            break

                                        fd.write(chunk)
                                        f += 1
                                        printProgressBar(f, int(size)/512 , prefix=f'Downloading chunk of 512 ko in progress', suffix= 'Chunk Complete', length=10, fill='x')
                                    fd.close()
                                print(f"img file:{fd.name} copied\n {i}/{len(links_for_download)} : {len(links_for_download)-i} remaining")
                                print(f"page {n}/{number_of_page} : {number_of_page-n} remaining")
                            else:
                                print(f"the file img/{dirname}/{filename}-page{n}-{i}.jpg already exists.")
                                print(f"skipping this url...")
                        i+=1
                        printProgressBar(i, len(links_for_download), prefix='Downloading Files in progress', suffix= 'Page Complete', length=50)
                        number_of_files+=1
                    print("===========================================================")
                    print(f'Page {n} has been scrapped entirely in folder {dirname}.')
                    if n < number_of_page:
                        print("===========================================================")
                        print(f' still {number_of_page-n} to scrap remaining...')
                    else:
                        print(f'==== LAST PAGE ({n/number_of_page}) ====')
                    print("===========================================================")
                    print(f'Scraping of page {n+1} started...')
                    print("==================================")
                    k+=1
                    printProgressBar(k+1, number_of_page, prefix='Downloading Page in progress', suffix= 'Page Complete', length=50)
            print("Done !")
            pages_for_keyword = key_word, f'{k} pages, {number_of_files} image files'
            summary.append(pages_for_keyword)
        print('Job Terminated successfully.')
        print('number of pages for each key word is :')
        for item in summary:
             print(f"{item}")
        print('Hope you enjoyed and Have fun with your new data !!!')
        self.flag_Thread_complete = True
        sys.exit(0)


def scrapping_iteration():
    pass


                




# for link in links_for_download:
#     url = requests.get(link)
#     soup = BeautifulSoup('url', 'lxml')
#     job = soup.find_all('img',{'id':'show_img'})
#     for link in job:
#         url_img = link.attrs['src']
#         myprint(url_img)


    




