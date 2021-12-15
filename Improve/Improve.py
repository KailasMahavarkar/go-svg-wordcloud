from time import time, sleep
import random


# def timesec(method):
#     try:
#         def timed(*args, **kw):
#             ts = time()
#             result = method(*args, **kw)
#             te = time()
#             print(method.__name__, int((te - ts) * 1000))
#             return result
#         return timed()
#     except Exception:
#         raise Exception("Error Occured")


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
    string = 'abcdefghijklmnopqrstuvwxyz0123456789'


    def timesec(method):
        try:
            def innerFunction(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                print(method.__name__, float((te - ts) / 1000))
                return result
            return innerFunction()
        except Exception as e:
            return e


    def genOTP(length=6):
        res = ''
        while len(res) != length:
            res += random.choice(string)
        return res


    def main():
        arr = []
        for x in range(10 ** 5):
            arr.append(getOTP(6))
        return arr


    res = timesec(main)
