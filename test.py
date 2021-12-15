# import requests
#
# def isFontAvailable(fontfamily):
#     fontfamily = " ".join([x.capitalize() for x in fontfamily.lower().split(' ')]).replace(' ', '%20')
#     try:
#         res = requests.get(f"https://fonts.googleapis.com/css?family={fontfamily}")
#         print(res.text)
#         if res.status_code != 200:
#             return "https://fonts.googleapis.com/css?family=Product%20Sans"
#     except Exception:
#         print()
#
# isFontAvailable(fontfamily="times new roman")


# print([[x for x in range(10)] for y in range(10)])

from itertools import permutations
# string = 'c..code..c...o.d.de'
string = 'abax'

newArr = []
for i, item in enumerate(string):
    if i in [3, 12, 13]:
        continue
    else:
        if item not in newArr:
            newArr.append(item)


newArr.remove('.')
print(newArr)












