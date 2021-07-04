import math
import numpy as np
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from svgPro.colorStop import negative, stopMax, correctedWords
from collections import Counter
from contextlib import contextmanager
import threading
import _thread
import random
import inflector
from Improve.Improve import timesec, executor
import aiohttp
import asyncio
import async_timeout


# controllers

async def get(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception:
            return ''

async def trigger(searchLinks: list, minlength: int = 3, maxlength: int = 15, timeout: int = 5):
    tasks = [asyncio.create_task(get(url=url)) for url in searchLinks]
    try:
        with async_timeout.timeout(timeout):
            await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        print('timed out')
        return "Request Closed by Timeout: {}"
    finally:
        master = []
        for i, task in enumerate(tasks):
            if task.done() and not task.cancelled():
                soup = BeautifulSoup(task.result(), "lxml")
                for word in str(soup.get_text()).replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').split(' '):
                    if minlength <= len(word) <= maxlength:
                        master.append(word)
        return master


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



def searchWordFilter(query: str = 'naruto', minlength: int = 3, maxlength: int = 10, stoptypes=None,
                     customlist=None, ignorelist=None, checknumeric: bool = False, minoccurence: int = 2,
                     factor: int = 50, sort: bool = True, mode: int = 1, singularize: bool = True, raw: bool = False):

    # 1 result = 0.5 sec
    if mode == 2:
        numresult = 18
        timeout = 9 + 2   # 2 second fault time
    elif mode == 3:
        numresult = 24
        timeout = 12 + 3   # 3 second fault time
    else:
        numresult = 8
        timeout = 4 + 1    # 1 second fault time


    if len(query) > 0:
        searchLinks = search(term=query, num_results=numresult)
        words = asyncio.run(trigger(minlength=minlength,maxlength=maxlength, searchLinks=searchLinks, timeout=timeout))
        return WordFilter(
            words=words,
            customlist=customlist,
            stoptypes=stoptypes,
            ignorelist=ignorelist,
            checknumeric=checknumeric,
            minoccurence=minoccurence,
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
    # print(f"Your OTP is {finalResult}")
    return finalResult



def WordFilter(words: list,  minlength: int = 3, maxlength: int = 10, stoptypes=None,
               customlist=None, ignorelist=None, checknumeric: bool = False, minoccurence: int = 2,
               factor: int = 50,  sort: bool = True, lengthcheck: bool = True, singularize: bool = True,
               raw: bool = False):

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
        stoptypes = ['basic', 'corrected']

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

    @timesec
    def main():
        res = searchWordFilter(
            query='robots',
            minlength=3,
            minoccurence=2,
            ignorelist=['autonomous'],
            stoptypes=['max', 'corrected'],
            mode=1,
            singularize=True,
            sort=True,
            raw=False,
        )

        print(res)



    main()



