from contextlib import suppress
from operator import ge
import random
from urllib.parse import urlparse
from dataFile import *
from colorStop import stopBasic, stopMax
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from timeit import default_timer as dt

import inflect
p = inflect.engine()
context = {}

def get_singular(plural_noun):
    plural = p.singular_noun(plural_noun)
    if (plural):
        return plural
    else:
        return plural_noun

class CRAWLER:
    def __init__(self,
                 query='pearl', pages=1, minWordLength=4, minWordOccurrence=4):
        self.context = {}
        self.query = query
        self.pages = pages
        self.stopwords = stopMax
        self.minWordLength = minWordLength
        self.minWordOccurrence = minWordOccurrence

    def getLinks(self):
        links = search(term=self.query,  num_results=8 * self.pages, lang='en')
        valid_links = []

        for link in links:
            with suppress(Exception) as e:
                result = urlparse(link)
                if (all([result.scheme, result.netloc])):
                    valid_links.append(link)
        return valid_links

    def getRawWords(self):
        words = []
        links = self.getLinks()
        
        for link in links:
            headers = requests.utils.default_headers()
            headers.update({
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            })

            sourcecode = requests.get(url=link)
            soup = BeautifulSoup(sourcecode.text, "lxml")
            page = str(soup.get_text()).split(' ')

            for word in page:
                word = word.lower()
                if len(word) >= self.minWordLength and word.isalpha() and word not in self.stopwords:
                    word = get_singular(word)
                    words.append(word)

        return words

    # def getContext(self):
    #     for word, freq in context.copy().items():
    #         if word[0: len(word) - 1] in context.keys():
    #             del context[word]
    #         if freq > self.minWordOccurrence:
    #             finalContext.update({word: int(math.log(freq, 50) * 70) + 1})

    #     finalContext = dict(sorted(finalContext.items(),
    #                         key=lambda item: item[1], reverse=True))
        
    #     if type(self.customFreq) == list:
    #         pump = 200
    #         temp = random.sample(population=self.customFreq, k=len(self.customFreq))[:200]
    #         for x in temp:
    #             if pump > 0:
    #                 self.context.update({x: int(math.log(pump, 50) * 70)})
    #                 pump -= random.choice([5, 4, 3, 2, 1])
    #     else:
    #         if not type(self.customFreq) == list:
    #             self.context = self.trigger()

    #     return self.context




from collections import Counter
import heapq

class Solution:
    def topKFrequent(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        if not nums:
            return []
        
        count = Counter(nums)
        
        h = []
        
        for i, num in enumerate(count.keys()):
            if i < k:
                heapq.heappush(h, (count[num], num))
            else:
                if h[0][0] < count[num]:
                    heapq.heappop(h)
                    heapq.heappush(h, (count[num], num))
                    
        res = []
        while h:
            _, n = heapq.heappop(h)
            res = [n] + res
        
        return res



if __name__ == '__main__':
    start = dt()
    x = CRAWLER(
        query='ios',
        pages=2,
        minWordLength=4,
        minWordOccurrence=4
    )

    ans = Solution().topKFrequent(x.getRawWords(), 50)
    print(ans  )
    

    end = dt()

    print(end - start)

