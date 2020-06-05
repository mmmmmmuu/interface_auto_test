# 轮询到完成
import json
import logging
import threading
import time
from copy import copy

import requests

from p4dao.dbDao import getAllInterfaceInfos
from p3db.Dboperator import Dboperator
from p2myconfig.config import *
from p5common.tempVariable import TempVariable


def runQuery(sql, interval, times):
    logging.debug("sql: " + sql + ";interval:" + str(interval) + ";times:" + str(times))
    dbops = Dboperator.getInstance()
    for i in range(times):
        dbops.end(option='commit')
        logging.debug("第" + str(i) + "次轮询开始:" + sql)
        num = dbops.getOne(sql)
        if num is not None and list(num.values())[0] >= 1:
            return True
        time.sleep(interval)
    return False


# 保留以前的借据
def lockLoan():
    dboperator = Dboperator.getInstance()
    dboperator.update("update acct_loan set lock_flag = 1;")


# def getSyndsByOrgid():
#     dboperator = Dboperator.getInstance()
#     return [item["syndicate_no"] for item in dboperator.getMany(
#         "select syndicate_no from {public_db}.acct_syndicate_info where org_no='{org_no}';".format(public_db=public_db, org_no=accountingOrgId))]


# 获取applyid
def getApplyId():
    '''获取唯一id'''
    return str(threading.get_ident()) + str(int(time.time() * 10000))


# 初始化日期
def initBusinessDate(businessdate):
    logging.debug("初始化日期开始...")
    logging.debug("businessDate:" + businessdate)
    dboperate = Dboperator.getInstance()
    # if selfcal:
    #     bookdate = businessdate
    # else:
    #     bookdate = datetime.datetime.strptime(businessdate, "%Y-%m-%d")
    #     delta = datetime.timedelta(days=1)
    #     bookdate = bookdate + delta
    #     bookdate = datetime.datetime.strftime(bookdate, "%Y-%m-%d")
    sql = "update " + cal_db + ".system_setup set business_date='" + businessdate + "',batch_date='" + businessdate + "',book_date='" + businessdate + "';"
    logging.debug("切日sql:" + sql)
    dboperate.update(sql)
    dboperate.update("truncate table bat_task_log;")
    logging.debug("初始化日期结束...")


def iter_replace(info, args, loc=None):
    if args:
        for key, value in args.items():
            if key in info.keys():
                if isinstance(value, dict) and info[key]:
                    iter_replace(info[key], value, loc)
                else:
                    info[key] = copy(value)
    info = replaceWithValue(info, loc=loc)
    return info


def replaceWithValue(args=None, loc=None):
    if not args:
        return args
    if isinstance(args, dict):
        result = {}
        for key, value in args.items():
            result[key] = replaceWithValue(args=value, loc=loc)
        return result
    elif isinstance(args, list):
        return [replaceWithValue(args=item, loc=loc) for item in args]
    else:
        return TempVariable.getValue(args, loc)


# 初始化场景参数
def initscene():
    scene = {}
    result = getAllInterfaceInfos()
    from myconfig.config import params
    for item in result:
        request_param = json.loads(item["request_param"])
        # request_param.update(params)
        scene[item["method_name"]] = {"requestType": item["request_type"], "desc": item["desc"], "params": request_param}
    return scene

def replace(origin, param):
    origin.update(param)
    return origin


if __name__ == '__main__':
    info = {'applyId': '{TIMESTAMP}', 'customerId': '{customerId}', 'customerName': '{customerName}', 'contractNo': '{contractNo}',
            'businessType': '{businessType}', 'productId': '{productId}', 'specificSerialNo': '{specificSerialNo}', 'businessSum': '',
            'currency': 'CNY', 'putoutDate': '2019-01-02', 'businessTerm': '3', 'businessRate': '{businessRate}', 'fineRate': '{fineRate}',
            'rptTermId': '{rptTermID}', 'defaultDueDay': None, 'graceDays': '3', 'firstDueDate': None, 'accountingOrgId': '{accountingOrgId}',
            'channelOrgId': '{channelOrgId}', 'syndicateSerialNo': None, 'selfAccountingFlag': '1', 'loansUsed': '010',
            'operateOrgId': '{operateOrgId}', 'putoutCouponDto': None,
            'flexiblePutoutSubsidyDto': {'subsidyInterestCalcType': 1, 'subsidyInterestCalcMode': 1, 'subsidyInterestBase': 2,
                                         'subsidyInterestRate': None, 'subsidyInterestAmount': None, 'orderAmount': None, 'subsidyEndDate': None},
            'rateList': [{'rateType': '01', 'businessRate': 12, 'beginDate': None, 'endDate': None},
                         {'rateType': '02', 'businessRate': 18, 'beginDate': None, 'endDate': None}],
            'rptList': [{'rptTermId': 'RPT-01', 'beginDate': None, 'endDate': None, 'segInstalmentAmt': None, 'restPaymentAmount': None}]}

    # info = {'businessRate': '{businessRate}', 'rateUnit': '01', 'businessSum': 10000, 'businessTerm': '3', 'putoutDate': '2019-01-02', 'rptTermID': '{rptTermID}', 'defaultDueDay': None, 'firstDueDate': None}

    args = {'businessSum': '', 'businessTerm': '3', 'defaultDueDay': None, 'syndicateSerialNo': None, 'putoutDate': '2019-01-02',
            'paymentDate': '2019-09-20',
            'flexiblePutoutSubsidyDto': {'subsidyInterestCalcType': 1, 'subsidyInterestCalcMode': 1, 'subsidyInterestBase': 2,
                                         'subsidyInterestRate': None, 'subsidyInterestAmount': None, 'orderAmount': None, 'subsidyEndDate': None},
            'applyId': '{TIMESTAMP}', 'customerId': '{customerId}', 'customerName': '{customerName}', 'contractNo': '{contractNo}',
            'businessType': '{businessType}', 'productId': '{productId}', 'specificSerialNo': '{specificSerialNo}', 'currency': 'CNY',
            'businessRate': '{businessRate}', 'fineRate': '{fineRate}', 'rptTermId': '{rptTermID}', 'graceDays': '3', 'firstDueDate': None,
            'accountingOrgId': '{accountingOrgId}', 'channelOrgId': '{channelOrgId}', 'selfAccountingFlag': '1', 'loansUsed': '010',
            'operateOrgId': '{operateOrgId}', 'putoutCouponDto': None,
            'rateList': [{'rateType': '01', 'businessRate': 12, 'beginDate': None, 'endDate': None},
                         {'rateType': '02', 'businessRate': 18, 'beginDate': None, 'endDate': None}],
            'rptList': [{'rptTermId': 'RPT-01', 'beginDate': None, 'endDate': None, 'segInstalmentAmt': None, 'restPaymentAmount': None}]}

    # iter_replace(info, args)
    print(TempVariable.getValue(key="{businessRate}", batch_no="20200520140658010827"))
