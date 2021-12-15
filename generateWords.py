import math
import random
import nltk
from nltk import tokenize, word_tokenize
import requests
import requests.exceptions
from bs4 import BeautifulSoup
from colorStop import *
from googlesearch import search
from wordfilter import WordFilter, singleWordFilter, searchWordFilter
import wikipedia
import datetime
import time
counter = 0
specials = ['/', "\\", '\n', '\t', ' ', '!', '"', '  # ', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

# random.sample(population=wordlist, k=len(wordlist))[:200]



if __name__ == '__main__':
    res = searchWordFilter(query='zenosama', stoptypes=['max', 'corrected', 'negative'])
    print(res)