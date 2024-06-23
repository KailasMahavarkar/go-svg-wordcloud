import requests.exceptions
from colorStop import *
from wordfilter import searchWordFilter
counter = 0
specials = ['/', "\\", '\n', '\t', ' ', '!', '"', '  # ', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']


if __name__ == '__main__':
    res = searchWordFilter(
        query='zenosama',
        stoptypes=['max', 'corrected', 'negative']
    )
    print(res)