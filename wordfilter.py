import math
import numpy as np
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from colorStop import negative, stopMax, correctedWords
from collections import Counter
from contextlib import contextmanager
import threading
import _thread
import random
import inflector
from helpers import timesec, executor
import aiohttp
import asyncio
import async_timeout
from typing import Union, List, AnyStr
import functools




def ignore_unhashable(func):
    uncached = func.__wrapped__
    attributes = functools.WRAPPER_ASSIGNMENTS + ('cache_info', 'cache_clear')

    @functools.wraps(func, assigned=attributes)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as error:
            if 'unhashable type' in str(error):
                return uncached(*args, **kwargs)
            raise

    wrapper.__uncached__ = uncached
    return wrapper


@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        print('timed out')
        return 'Timed out'
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()


def searchWordFilter(query: str = 'naruto', links: List = None, minlength: int = 3, maxlength: int = 10, stoptypes=None,
                     customlist=None, ignorelist=None, checknumeric: bool = False, minoccurence: int = 2,
                     factor: int = 50, sort: bool = True, mode: int = 1, singularize: bool = True, raw: bool = False):

    # 1 result = 0.5 sec
    if mode == 2:
        numresult = 18
        timeout = 9 + 2  # 2 second tolerance
    elif mode == 3:
        numresult = 24
        timeout = 12 + 3  # 3 second tolerance
    elif mode == 4:
        numresult = 36
        timeout = 18 + 4  # 4 second tolerance
    else:
        numresult = 8
        timeout = 4 + 1  # 1 second tolerance

    if len(query) > 0:
        if links is not None:
            searchLinks = links
        else:
            searchLinks = search(term=query, num_results=numresult)

        allwords = []
        for link in searchLinks:
            try:
                with time_limit(timeout):
                    response = requests.get(link)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    words = text.split()
                    allwords.extend(words)
            except Exception as e:
                print(f"Error occurred: {e}")
        

        return WordFilter(
            words=allwords,
            customlist=customlist,
            stoptypes=stoptypes,
            ignorelist=ignorelist,
            checknumeric=checknumeric,
            minoccurence=minoccurence,
            minlength=minlength,
            maxlength=maxlength,
            factor=factor,
            sort=sort,
            raw=raw,
            lengthcheck=False,
            singularize=singularize
        )


def searchWordFilterWrapper(query: str = 'naruto', minlength: int = 3, maxlength: int = 10, stoptypes=None,
                            customlist=None, ignorelist=None, checknumeric: bool = False, minoccurence: int = 2,
                            factor: int = 50, sort: bool = True, mode: int = 1, singularize: bool = True,
                            raw: bool = False):
    return executor(searchWordFilter, query, minlength, maxlength, stoptypes, customlist, ignorelist,
                    checknumeric, minoccurence, factor, sort, mode, singularize, raw)


def singleWordFilter(word: str, stoptypes: list, minlength: int = 3, maxlength: int = 10,
                     customlist=None, ignorelist=None, checknumeric: bool = False, lengthcheck: bool = True):
    """
    :param word: word string to check
    :param minlength: 3
    :param maxlength: 10
    :param stoptypes: default basic & custom
    :param customlist: default empty list
    :param ignorelist: default empty list
    :param checknumeric: default False
    :param lengthcheck: ignore lengthcheck
    :return: bool
    """

    # ignore list check
    if word in ignorelist:
        return True

    # wordlength check
    if lengthcheck:
        if not minlength <= len(word) <= maxlength:
            return False

    # checking stopmax
    if 'max' in stoptypes:
        if word in stopMax:
            return False

    # checking corrected words
    if 'corrected' in stoptypes:
        if word in correctedWords:
            return False

    # checking negative words
    if 'negative' in stoptypes:
        if word in negative:
            return False

    if len(customlist) > 0:
        if word in customlist:
            return False

    if checknumeric:
        if not all([k.isalnum() for k in word]):
            return False
    else:
        if not all([k.isalpha() and k.isascii() for k in word]):
            return False

    return True


def getOTP(maxlength=6):
    possibleCharacters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    result = []
    for x in range(maxlength):
        randomChar = random.choice(possibleCharacters)
        result.append(randomChar)

    finalResult = ''.join(result)
    return finalResult


def WordFilter(words: list, minlength: int = 3, maxlength: int = 10, stoptypes=None,
               customlist=None, ignorelist=None, checknumeric: bool = False, minoccurence: int = 2,
               factor: int = 50, sort: bool = True, lengthcheck: bool = True, singularize: bool = True,
               raw: bool = False) -> object:
    """
    :param words: list of words
    :param minlength: 3
    :param maxlength: 10
    :param stoptypes: default basic & custom
    :param customlist: default empty list
    :param ignorelist: default empty list
    :param checknumeric: False
    :param factor: 50
    :param minoccurence: 2
    :param sort: default True
    :param lengthcheck: default True
    :param singularize: default True
    :param raw: default False
    :return: filtered list of words
    """

    # store result of wordfilter
    result = []

    # initially stoptypes list is set to basic
    if stoptypes is None:
        stoptypes = ['basic', 'corrected', 'stopmax', 'negative']

    # initially customlist list is empty
    if customlist is None:
        customlist = []

    # initially ignorelist is empty
    if ignorelist is None:
        ignorelist = []

    for word in words:
        if singleWordFilter(
                word=word.lower(),
                minlength=minlength,
                maxlength=maxlength,
                stoptypes=stoptypes,
                customlist=customlist,
                ignorelist=ignorelist,
                checknumeric=checknumeric,
                lengthcheck=lengthcheck
        ):
            result.append(word.lower())


    if singularize:
        singularizedList = []
        for word in result:
            if word not in ignorelist:
                singularizedResult = inflector.English().singularize(word=word)
                singularizedList.append(singularizedResult)
            else:
                singularizedList.append(word)
        context = dict(Counter(singularizedList))
    else:
        context = dict(Counter(result))

    # raw 0 | sort 0
    if raw is False and sort is False:
        return {key: int(math.log(value, factor) * 70) for key, value in context.items() if value >= minoccurence}

    # raw 0 | sort 1 --> default
    if raw is False and sort is True:
        context = sorted(context.items(), key=lambda x: x[1], reverse=True)
        return {key: int(math.log(value, factor) * 70) for key, value in context if value >= minoccurence}

    # raw 1 | sort = 0
    if raw is True and sort is False:
        return {key: value for key, value in context.items() if value >= minoccurence}

    # raw 1 | sort = 1
    if raw and sort:
        context = sorted(context.items(), key=lambda x: x[1], reverse=True)
        return {key: value for key, value in context if value >= minoccurence}


if __name__ == '__main__':
    gigTeaching = ""

    # @ignore_unhashable
    # @functools.lru_cache(6)

    # @timesec
    def main(query="piracy"):
        print("started ....")

        print(WordFilter(
            words=['human',  'human', 'bello', "the", "the", 'buffello'],
            stoptypes=['max', 'negative'],
        ))

        # res = searchWordFilter(
        #     query=query,
        #     minlength=3,
        #     maxlength=10,
        #     minoccurence=1,
        #     ignorelist=[],
        #     mode=4,
        #     stoptypes=['max', 'corrected', 'stopmax', 'negative'],
        #     # singularize=True,
        #     sort=True,
        #     raw=False,
        # )
        # ie = []
        # for k, v in res.items():
        #     if v > 0:
        #         ie.append(k)
        # print(", ".join(ie))

    main("pirates")
