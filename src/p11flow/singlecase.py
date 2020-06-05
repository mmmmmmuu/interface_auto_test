from copy import copy

from control.Control import *
import logging
from myconfig import config


def putout(params=None):
    # lockLoan()
    params = params if params else {"businessSum": 100000, "businessTerm": 3, "defaultDueDay": "25", "syndicateSerialNo": "56010002",
                                    "putoutDate": "2019-09-20", "dbflag": True}
    serialno = flexiblePouout(params)
    print(serialno)
    # 392333245171122184


def putout_task_pay(params=None):
    lockLoan()
    params = params if params else {"businessSum": 100000, "businessTerm": 3, "defaultDueDay": "25", "syndicateSerialNo": "56010002",
                                    "putoutDate": "2019-09-20", "dbflag": True}
    serialno = flexiblePouout(params)
    print(serialno)
    runCommonInterface("endOfDayAllToDate", params)
    params["loanSerialNo"] = serialno
    print(serialno)
    payback(copy(params))
    # 392312388809932813


def normalpayback(params=None):
    lockLoan()
    params = params if params else {"businessSum": 100000, "businessTerm": 3, "defaultDueDay": "25", "syndicateSerialNo": "56010002",
                                    "putoutDate": "2019-09-20", "dbflag": True}
    serialno = flexiblePouout(params)
    print(serialno)
    runCommonInterface("endOfDayAllToDate", params)
    params["loanSerialNo"] = serialno
    print(serialno)
    payback(copy(params))
    params["toBusinessDate"] = "2019-11-25"
    runCommonInterface("endOfDayAllToDate", params)
    payback(copy(params))
    params["toBusinessDate"] = "2019-12-20"
    runCommonInterface("endOfDayAllToDate", params)
    # payback(copy(params))
    payback({"loanSerialNo": serialno, "transCode": "2002"})
    print(serialno)


def runtask():
    runCommonInterface("endOfDayAllToDate", {"toBusinessDate": "2019-09-25"})


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET,
                        format='%(levelname)s-%(thread)d:%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d]: %(message)s')  # 设置日志级别
    # prepaynowterm()
    params = {}
    params = {"businessSum": 100000, "businessTerm": 3, "defaultDueDay": "25", "syndicateSerialNo": "52010001", "putoutDate": "2020-07-25",
              "dbflag": True}
    # # params.update(config.params)
    params["toBusinessDate"] = "2020-08-25"
    params["transCode"] = "2001"
    # # params["prePayType"] = "4"
    putout_task_pay(params)
    # lockLoan()
    # putout(params)
    # putout(params)
    # putout(params)
    # putout(params)
    # putout(params)
    # normalpayback(params)
    # runCommonInterface("endOfDayAllToDate", params)
    # params["loanSerialNo"] = "402777686511992850"
    # payback(copy(params))
    # params["transCode"] = "2002"
    # payback(copy(params))
