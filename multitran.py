import re
from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
PATH  = 'https://www.multitran.com/m.exe' 

class MultitranWord(object):
    def __init__(self, s='hello', l1=1, l2=2):
        self.word = s
        self._l1 = l1
        self._l2 = l2
        params = dict(
            s = s,
            l1 = l1,
            l2 = l2)
        self._page = get(PATH, params = params)
        if not self._page.ok:
            raise ValueError
        self._page.encoding = 'utf-8'
        self._html = BeautifulSoup(
            self._page.text,
            features="html.parser")
        self.transcription = self._html.select_one('td.gray')
        if self.transcription:
            self.transcription = re.search(
                r'(\[.+\])', 
                self.transcription.get_text() )
            if self.transcription:
                self.transcription = self.transcription.group(1)
        self.translations = self._html.select('td.trans')

if __name__ == "__main__":
    while True:
        word_string = input('enter a word: ')
        for word in word_string.split():
            translate = MultitranWord(word)
            print('', end = word)
            print('\t', end = translate.transcription)
            print()
            for tag in translate.translations:
                try:
                    pprint(tag.get_text())
                    input('\n', width = 70)
                except KeyboardInterrupt:
                    print()
                    break
