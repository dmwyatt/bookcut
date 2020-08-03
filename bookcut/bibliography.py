import requests
from bs4 import BeautifulSoup as Soup
import json
import re
from difflib import SequenceMatcher
import os


def similar(a, b, similarity):
    ''' function which check similarity between two strings '''
    ratio = SequenceMatcher(None, a, b).ratio()
    if ratio > similarity and ratio < 1:
        return True
    else:
        return False


def main(author, similarity):
    search_url = "http://openlibrary.org/search.json?author=" + author
    jason = requests.get(search_url)
    jason = jason.text
    data = json.loads(jason)
    data = data['docs']
    if data != []:
        metr = 0
        books = []
        for i in range(0, len(data)-1):
            title = data[metr]['title']
            metr = metr + 1
            books.append(title)
            mylist = list(dict.fromkeys(books))

    #       Filtrering results: trying to erase similar titles
        words = [' the ', 'The ', ' THE ', ' The' ' a ', ' A ', ' and ', ' of ',
                 ' from ', 'on', 'The', 'in']

        noise_re = re.compile('\\b(%s)\\W'%('|'.join(map(re.escape,words))),re.I)
        clean_mylist = [noise_re.sub('',p) for p in mylist]


        for i in clean_mylist:
            for j in clean_mylist:
                a = similar(i,j, similarity)
                if a == True:
                    clean_mylist.pop(a)

        clean_mylist.sort()
        print(' ~Books found to OpenLibrary Database:\n')
        for i in clean_mylist:
            print(i)
        return clean_mylist
    else:
        print('(!) No valid author name, or bad internet connection.')
        print('Please try again!')
        return None

def save_to_txt(lista, path, author):
    for content in lista:
        name = f'{author}_bibliography.txt'
        full_path = os.path.join(path, name)
        with open(full_path, 'a', encoding='utf-8') as f1:
            f1.write(content + ' ' + author + os.linesep)
    print('\nList saved at: ', full_path, '\n')




if __name__ == '__main__':

    ins = input('Name: ')
    main(ins)
