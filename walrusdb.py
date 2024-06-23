from walrus import *
import dataFile as df


class WalrusDB:
    def __init__(self) -> None:
        self.key = "svgpro:datafile"
        self.db = Walrus(
            host="redis-14316.c264.ap-south-1-1.ec2.cloud.redislabs.com",
            port=14316,
            password="Shared@123!",
            db=0
        )

    def setHashNX(self, key, object):
        hash = self.db.Hash(self.key)
        return hash.setnx(key, json.dumps(object))

    def setHash(self, key, object):
        try:
            hash = self.db.Hash(self.key)
            hash.__setitem__(key, json.dumps(object))
            return True
        except Exception as e:
            raise e

    def getHash(self, key: str):
        hash = self.db.Hash(self.key)
        return json.loads(str(hash.get(key), encoding='utf-8'))


if __name__ == "__main__":
    # ----------- START: CELERY  --------------
    # app = Celery('hello', broker=red)
    # @app.task
    # def foo(text):
    #     time.sleep(5)
    #     return text[::-1]
    # result = foo.delay("kai")
    # ----------- END: CELERY --------------
    zero = WalrusDB()

    def syncDB():
        moduleObject = ({item: getattr(df, item) for item in dir(df)
                         if not item.startswith("__") and not item.endswith("__")})
        for key, value in moduleObject.items():
            try:
                zero.setHashNX(key, value)
            except Exception as e:
                print("error in key", key)

    def goodSync():
        pass
