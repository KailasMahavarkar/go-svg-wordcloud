from string import punctuation, ascii_letters
from svgPro.dataFile import *
from svgPro.colorStop import *
from bs4 import BeautifulSoup
import requests
import math
from googlesearch import search
from timeit import default_timer as dt
import numpy as np

context = {}


class CRAWLER:
    def __init__(self, query='pearl', customFreq=None, pages=1, stopType=stopBasic, minWordLength=4,
                 minWordOccurrence=4):
        self.context = {}
        self.query = query
        self.customFreq = customFreq
        self.stopType = stopType
        self.pages = pages
        self.minWordLength = minWordLength
        self.minWordOccurrence = minWordOccurrence
        self.customStop = customStop

    def trigger(self):
        genLinks = search(self.query, tld="com", num=8 * self.pages, stop=8 * self.pages, pause=0)

        finalContext = {}
        for link in genLinks:
            headers = requests.utils.default_headers()
            headers.update({
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            })

            sourcecode = requests.get(url=link)
            plaintext = sourcecode.text
            soup = BeautifulSoup(plaintext, "html.parser")
            page = str(soup.get_text()).split(' ')

            for word in page:
                word = word.lower()
                if len(word) >= self.minWordLength and word.isalpha() and word not in self.stopType.keys() and word not in customStop.keys():
                    if word not in context.keys():
                        context.update({word: 1})
                    else:
                        context.update({word: context[word] + 1})

        for word, freq in context.copy().items():
            if word[0: len(word) - 1] in context.keys():
                del context[word]
            if freq > self.minWordOccurrence:
                finalContext.update({word: int(math.log(freq, 50) * 70) + 1})

        finalContext = dict(sorted(finalContext.items(), key=lambda item: item[1], reverse=True))
        return finalContext

    def getContext(self):
        if type(self.customFreq) == list:
            pump = 200
            temp = random.sample(population=self.customFreq, k=len(self.customFreq))[:200]
            for x in temp:
                if pump > 0:
                    self.context.update({x: int(math.log(pump, 50) * 70)})
                    pump -= random.choice([5, 4, 3, 2, 1])
        else:
            if not type(self.customFreq) == list:
                self.context = self.trigger()

        return self.context


if __name__ == '__main__':
    start = dt()
    x = CRAWLER(
        query='ios',
        pages=2,
        minWordLength=4,
        minWordOccurrence=4
    ).getContext()

    print(x)
    end = dt()

    print(end - start)
