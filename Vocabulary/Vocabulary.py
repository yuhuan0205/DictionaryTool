from bs4 import BeautifulSoup
from playsound import playsound
import requests

class Vocabulary:
    def __init__(self, word):
        self.word = word
        self.chinese = []
        self.change = []
        self.example = []
        
    def lookUp(self):
        self.chinese = []
        self.change = []
        self.example = []        
        if self.word[-3:] == 'ies':
            self.word = self.word[0:-3]+'y'
        r = requests.get(f'https://tw.dictionary.search.yahoo.com/search;?fr2=sb-top-tw.dictionary.search&fr=sfp&p={self.word}') 
        r = r.text
        soup = BeautifulSoup(r, 'html.parser')
        
        try:
            self.chinese = soup.find('div',class_ = 'compList mb-25 p-rel').find_all('div')
        except AttributeError:
            pass
        try:
            self.change = soup.find('ul',class_ = 'compArticleList pt-18 pl-25 pr-25 pb-18 bg-fafafc bt-1-e5').find_all('span')
        except AttributeError:
            pass
        try:
            self.example = soup.find('div',class_ = 'compTextList ml-50').find_all('li')
        except AttributeError:
            pass
    
    def save(self):
        self.lookUp()
        f = open("vocabulary.txt", "a")
        f.write(self.word+"\n")
        f.close()

    def insert(self,text):
        text.insert('insert',self.word+"\n\n",'tag_2')
        try:
            for i in range(0,len(self.chinese),2):
                text.insert('insert',self.chinese[i].text + " " + self.chinese[i+1].text + "\n",'tag_1')
        except IndexError:
            for i in range(0,len(self.chinese),2):
                text.insert('insert',self.chinese[i].text + "\n",'tag_1')

        text.insert('insert',"\n動詞變化\n\n",'tag_2')
        for i in self.change:
            text.insert('insert',i.text + "\n",'tag_1')
        text.insert('insert',"\n例句\n\n",'tag_2')
        for i in self.example:
            text.insert('insert',i.text + "\n",'tag_1')

    def playSound(self):
        playsound(f'https://s.yimg.com/bg/dict/dreye/live/m/{(self.word).strip().lower()}.mp3')