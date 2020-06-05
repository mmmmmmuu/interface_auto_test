from db.Dboperator import Dboperator
from executor.InterfaceRunner import getBusinessDate
from myconfig.config import tiexi_rate, cal_db
from service.common import runCommonInterface
from tools.utils import *

# 放款
from tools.utils import getApplyId, initBusinessDate, lockLoan

'''
dbflag: true 初始化日期
'''

def pouout(args):
    '''放款'''
    return myputout(args=args, apply_method="putoutApply")

# 灵活放款
'''
dbflag: true 初始化日期
'''
def flexiblePouout(args):
    return myputout(args=args, apply_method="flexiblePutoutApply")

# 放款统一封装
def myputout(args, apply_method):
    '''放款'''
    args["applyId"] = getApplyId()
    dboperate = Dboperator.getInstance()
    if "dbflag" in args.keys() and args["dbflag"] and "putoutDate" in args.keys() and args["putoutDate"] is not None and args["putoutDate"] != '':
        initBusinessDate(args["putoutDate"])
    elif "putoutDate" not in args.keys() or args["putoutDate"] is None or args["putoutDate"] == '':
        args["putoutDate"] = getBusinessDate()
    runCommonInterface("putoutTrial", args, flag=True)
    if apply_method == "flexiblePutoutApply" and "flexiblePutoutSubsidyDto" not in args.keys():
        args["flexiblePutoutSubsidyDto"] = {"subsidyInterestRate": tiexi_rate[int(args["businessTerm"])],
                                            "subsidyInterestAmount": int(args["businessSum"]) * 1.2 * tiexi_rate[int(args["businessTerm"])] / 100,
                                            "orderAmount": int(args["businessSum"]) * 1.2}
        # args["flexiblePutoutSubsidyDto"] = {"subsidyInterestRate": tiexi_rate[int(args["businessTerm"])],
        #                                     "subsidyInterestAmount": 407.50,
        #                                     "orderAmount": int(args["businessSum"]) * 1.2}
    rev = runCommonInterface(apply_method, args, flag=True)
    result = json.loads(rev.content)
    rev = runCommonInterface("executeTransaction", {"transactionId": result["transactionId"], "transCode": "1001", "paymentDate": args["putoutDate"],
                                                    "loanSerialNo": result["loanSerialNo"]}, flag=True, tranName="放款")
    result = json.loads(rev.content)
    loanSerialNo = result["loanSerialNo"]
    # if needpentinter:
    #     sql = "INSERT INTO " + cal_db + ".acct_loan_rate_segment (id, serialno, product_no, object_type, object_no, term_id, seg_from_date, seg_to_date, status, rate_type, rate_unit, base_rate_type, base_rate, rate_float, business_rate, year_base_day, relative_type, relative_id, create_time) \
    #              VALUES (" + args["applyId"] + ",'" + args["applyId"] + "', " + productId + ", '', '', 2, '" + args[
    #         "putoutDate"] + "', null, 1, '03', '01', '1', 12.00000000, 50.00000000, 18.00000000, 360, 1, (select id from " + cal_db + ".acct_loan where  serialno = '" + \
    #           result["loanSerialNo"] + "'), now());"
    #     logging.info("复利sql:---- " + sql)
    #     dboperate.insert(sql)
    return loanSerialNo

# 还款
def payback(args):
    '''还款'''
    # 系统日期
    businessdate = getBusinessDate()
    # businessdate='2021-10-18'
    if args["loanSerialNo"] is None:
        raise RuntimeError(args["loanSerialNo"] + "借据号不存在！")
    if "businessDate" not in args.keys() or args["businessDate"] is None or args["businessDate"] == "":
        args["businessDate"] = businessdate
    # dboperate = Dboperator()
    # 日志提示
    desc = ''
    # ntermFlag=False
    amt = 0 if "amt" not in args else args["amt"]
    if "2001" == args['transCode']:
        desc = "正常/逾期"
        args["prePayType"] = 0
        args["prePayInterestDaysFlag"] = 0
        args["prePayInterestBaseFlag"] = 0
        args["prePayAmtFlag"] = 0
        rev = runCommonInterface("paymentTrial", args, flag=True)
        result = json.loads(rev.content)
        if amt == 0 or amt == '0' or amt is None or amt == '':
            amt = result["payAmt"]
    elif "2002" == args['transCode'] or "2010" == args['transCode']:
        desc = "提前"
        if "prePayType" in args.keys() and (args["prePayType"] == "4" or args["prePayType"] == 4):
            desc = "提前还当期"
            args["prePayAmtFlag"] = 1
        result = runCommonInterface("prepaymentTrial", args, flag=True)
        if amt == 0 or amt == '0' or amt is None or amt == '':
            amt = json.loads(result.content)["actualPayAmt"]
    args["amt"] = amt
    args["applyId"] = getApplyId()
    logging.debug(desc + "还款参数为：" + str(args))
    rev = runCommonInterface("paymentApply", args, flag=True, tranName=desc)
    result = json.loads(rev.content)
    args["transactionId"] = result["transactionId"]
    if "paymentDate" not in args.keys() or args["paymentDate"] is None or args["paymentDate"] == "":
        args["paymentDate"] = businessdate
    runCommonInterface("executeTransaction", args, flag=True, tranName=desc)
    logging.debug(args["loanSerialNo"] + desc + "还款完成！")

# 退货
def returnGoods(args):
    '''还款'''
    if args["loanSerialNo"] is None:
        raise RuntimeError(args["loanSerialNo"] + "借据号不存在！")
    desc = ''

    amt = 0 if "amt" not in args else args["amt"]
    if "2001" == args['transCode']:
        desc = "正常/逾期"
        rev = runCommonInterface("paymentTrial", args, flag=True)
        result = json.loads(rev.content)
        if amt == 0 or amt == '0' or amt is None or amt == '':
            amt = result["payAmt"]
        args["amt"] = amt
    elif "2002" == args['transCode']:
        desc = "提前"
        runCommonInterface("prepaymentTrial", args, flag=True)
    args["applyId"] = getApplyId()
    logging.debug(desc + "还款参数为：" + str(args))
    rev = runCommonInterface("paymentApply", args, flag=True, tranName=desc)
    result = json.loads(rev.content)
    args["transactionId"] = result["transactionId"]
    runCommonInterface("executeTransaction", args, flag=True, tranName=desc)
    logging.debug(args["loanSerialNo"] + desc + "还款完成！")


if __name__ == '__main__':
    # logging.getLogger().setLevel(logging.DEBUG)
    # print(getBusinessDate())
    # input()
    logging.basicConfig(level=logging.NOTSET,
                        format='%(levelname)s-%(thread)d:%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d]: %(message)s')  # 设置日志级别
    # cleanDb(dbnames='calculator')
    # result = getBusinessDate()
    # print(result)
    # initDb = initDb()
    # initDb.initDb()
    # dbopr = Dboperator()
    # sql = "select * from acct_loan;"
    # logging.info("-------------")
    # for i in range(100):endOfDayAllToDate
    #     dbopr.getAll(sql=sql)
    # logging.info("-------------")
    # rev = runCommonInterface("putoutTrial",defaultDueDay="02")
    # rev = endOfDayAll("endOfDayAll",productid="5301")
    # print(rev.content)
    # initBusinessDate('2019-06-12')
    lockLoan()
    # serialno = pouout({"businessSum": 10000, "businessTerm": 3, "defaultDueDay": "20", "syndicateSerialNo": "", "putoutDate": "2019-09-20", "dbflag": True})
    # serialno = flexiblePouout({"businessSum": 10000, "businessTerm": 3, "defaultDueDay": "20", "syndicateSerialNo": "56010002", "putoutDate": "2019-09-20", "dbflag": True})
    serialno = flexiblePouout({"businessSum": 10000, "businessTerm": 3, "defaultDueDay": "30", "syndicateSerialNo": "56010002", "putoutDate": "2019-09-20", "dbflag": True})
    # serialno = pouout({"businessSum": 10000, "businessTerm": 12, "defaultDueDay": "20", "syndicateSerialNo": "", "putoutDate": "2019-09-20", "dbflag": True})
    runCommonInterface("endOfDayAllToDate", {"toBusinessDate": "2019-09-30"})
    # serialno = pouout({"businessSum":600, "businessTerm":12,"syndicateSerialNo": "","putoutDate   ":"2018-08-02","rptTermId":'RPT-01',"defaultDueDay":"02","businessRate": "21.6", "fineRate": "32.4","dbflag":True})
    # serialno1 = pouout({"businessSum":3000, "businessTerm":3, "defaultDueDay":"15","syndicateSerialNo": "","putoutDate":"2019-06-15","dbflag":True})
    payback({"loanSerialNo": serialno, "transCode": "2002"})
    # serialno1 = pouout({"businessSum":5000, "businessTerm":12, "defaultDueDay":"15","syndicateSerialNo": "","putoutDate":"2019-06-15"})
    # cleanDb()
    # serialno = pouout({"businessSum": 25000, "businessTerm": 6, "defaultDueDay": "02","syndicateSerialNo": "10091003","putoutDate": "2019-02-28","dbflag":True})
    # time.sleep(18)
    # runCommonInterface("endOfDayAllToDate",{"toBusinessDate":"2019-07-19"})
    # payback({"loanSerialNo": '186975190709190659',"transCode":"2002","prePayType":4})
    # payback({"loanSerialNo": serialno,"transCode":"2002","payRuleType":"01"})
    # payback({"businessDate":"2019-05-19","loanSerialNo":serialno2,"transCode":"2002","paymentDate":"2019-05-19","prePayType":4,"prepayInterestDaysFlag":2})
    # payback({"businessDate":"2019-06-23","loanSerialNo":'176555935056494593',"transCode":"2001","paymentDate":"2019-06-23"})
    # serialno='181164546634252292'
    # runCommonInterface("endOfDayAllToDate",{"toBusinessDate":"2018-09-02"})
    # payback({"loanSerialNo":'189534716340314121',"transCode":"2001"})

    # runCommonInterface("endOfDayAllToDate",{"toBusinessDate":"2018-10-02"})
    # payback({"loanSerialNo":serialno,"transCode":"2001"})

    print(serialno)
    # print(serialno1)
    # payback({"transCode":"2001", "loanSerialNo":"73994005813223428","businessDate": "2019-02-02"})
    # print(runQuery("select count(1) from cfs.acct_loan where loanstatus = '9';",1,120))
#  https://www.cnblogs.com/CJOKER/p/8295272.htmlselect * from acct_loan where loanstatus = 9
