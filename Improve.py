from time import time, sleep
import random

def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.5f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed


def timesec(method):
    try:
        def timed(*args, **kw):
            ts = time()
            result = method(*args, **kw)
            te = time()
            if 'log_time' in kw:
                name = kw.get('log_name', method.__name__.upper())
                kw['log_time'][name] = int((te - ts) * 1000)
            else:
                print('%r  %2.5f s' % (method.__name__, (te - ts)))
            return result
        return timed
    except Exception:
        raise Exception("Error Occured")


def executorClosure(method):
    def inner(*args, **kwargs):
        return method(*args, **kwargs)
    return inner


def executor(method, *args, **kwargs):
    def inner():
        return method(*args, *kwargs)
    return inner


def getOTP(maxlength=6):
    possibleCharacters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    result = []
    for x in range(maxlength):
        randomChar = random.choice(possibleCharacters)
        result.append(randomChar)

    finalResult = ''.join(result)
    # print(f"Your OTP is {finalResult}")
    return finalResult


if __name__ == '__main__':
    def sub(a, b):
        return f'sum:  {a - b}'

    for x in range(13):
        print(f'Question no {x} : 10')
