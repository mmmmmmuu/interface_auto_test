import datetime
import threading
from copy import copy


class TempVariable:
    cage = {"scene": {}}

    @classmethod
    def addToBatch(cls, value, batch_no=None):
        if not value:
            return
        if not batch_no:
            cls.cage.update(value)
        else:
            if batch_no not in cls.cage.keys():
                cls.cage[batch_no] = {}
            cls.cage[batch_no].update(value)

    @classmethod
    def saveValue(cls, key, value, loc=None):
        if not loc:
            cls.cage[key] = value
            return
        resp = cls.cage
        for index in loc.split("."):
            resp = resp[index]
        resp[key] = value

    @classmethod
    def saveParam(cls, value, loc=None):
        if not loc:
            cls.cage["__param"].update(value)
            return
        resp = cls.cage
        for index in loc.split("."):
            resp = resp[index]
        resp["__param"] = copy(value)

    @classmethod
    def saveResponse(cls, value, loc=None):
        if not loc:
            cls.cage["__response"].update(value)
            return
        resp = cls.cage
        for index in loc.split("."):
            resp = resp[index]
        resp["__response"] = copy(value)

    @classmethod
    def updateResponse(cls, value, loc=None):
        if not loc:
            cls.cage["__response"].update(value)
            return
        resp = cls.cage
        for index in loc.split("."):
            resp = resp[index]
        if "__response" not in resp.keys():
            resp["__response"] = copy(value)
        else:
            resp["__response"].update(value)

    @classmethod
    def saveAction(cls, value, loc=None):
        if not loc:
            cls.cage["__action"].update(value)
            return
        resp = cls.cage
        for index in loc.split("."):
            resp = resp[index]
        if "__action" not in resp.keys():
            resp["__action"] = copy(value)
        else:
            resp["__action"].update(value)

    @classmethod
    def getValue(cls, key, loc=None):
        cls.cage["TIMESTAMP"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        cls.cage["RANDOM_STR"] = str(threading.get_ident()) + '-' + cls.cage["TIMESTAMP"]

        def searchkey(key, cage):
            if "__response" in cage.keys() and key in cage["__response"].keys():
                return cage["__response"][key]
            elif "__action" in cage.keys() and key in cage["__action"].keys():
                return cage["__action"][key]
            elif key in cage.keys():
                return cage[key]
            return None

        def searchkeys(keys, cage):
            key = keys[-1]
            del keys[-1]
            try:
                for index in keys:
                    cage = cage[index]
                return searchkey(key, cage)
            except KeyError:
                return None

        if key and isinstance(key, str) and key.startswith("{") and key.endswith("}"):
            keys = key.replace("{", '', 1).replace("}", '', 1).strip().split(".")
            searchlist = [cls.cage]
            if loc:
                for index in loc.split("."):
                    if index in searchlist[-1].keys():
                        searchlist.append(searchlist[-1][index])
                    else:
                        return None
            for item in searchlist[::-1]:
                value = searchkeys(copy(keys), copy(item))
                if value:
                    return value
            else:
                return None
        return key

    @classmethod
    def initResp(cls, loc):
        resp = cls.cage
        for index in loc.split("."):
            if index not in resp.keys():
                resp[index] = {"__param": {}, "__response": {}, "__action": {}}
            resp = resp[index]

    @classmethod
    def cleanBatch(cls, batch_no):
        del cls.cage[batch_no]


if __name__ == '__main__':
    result = TempVariable.getValue("{payAmt}", loc="")
    print(result)
