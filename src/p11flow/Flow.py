import datetime

from myconfig.config import model
from control.Control import *
from tools.Tools import *

from db.product_db_opr import clean_db
from db.test_db_opr import cleanbatch
from selfenum import TractionType
from tools.flow_control import getBatchInfo, runModel, saveBatchInfo
from tools.get_info_by_excel import getdatalistfromexcel, getscenefromexcel
from tools.tools import getSyndsByOrgid

dataList = {
    'loan1': {'businessSum': '10000 ', 'businessTerm': '3', 'defaultDueDay': '15'},
    'loan2': {'businessSum': '11000 ', 'businessTerm': '12', 'defaultDueDay': '15'},
    'loan3': {'businessSum': '12000 ', 'businessTerm': '3', 'defaultDueDay': '15'},
    'loan4': {'businessSum': '13000 ', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan5': {'businessSum': '14000 ', 'businessTerm': '3', 'defaultDueDay': '12'},
    'loan6': {'businessSum': '15000 ', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan7': {'businessSum': '16000 ', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan8': {'businessSum': '17000 ', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan9': {'businessSum': '18000 ', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan10': {'businessSum': '190000', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan11': {'businessSum': '200000', 'businessTerm': '3', 'defaultDueDay': '12'},
    'loan12': {'businessSum': '210000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan13': {'businessSum': '220000', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan14': {'businessSum': '230000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan15': {'businessSum': '240000', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan16': {'businessSum': '250000', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan17': {'businessSum': '260000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan18': {'businessSum': '270000', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan19': {'businessSum': '280000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan20': {'businessSum': '290000', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan21': {'businessSum': '300000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan22': {'businessSum': '310000', 'businessTerm': '3', 'defaultDueDay': '02'},
    'loan23': {'businessSum': '320000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan24': {'businessSum': '330000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan25': {'businessSum': '340000', 'businessTerm': '6', 'defaultDueDay': '02'},
    'loan26': {'businessSum': '350000', 'businessTerm': '12', 'defaultDueDay': '02'},
    'loan27': {'businessSum': '360000', 'businessTerm': '24', 'defaultDueDay': '02'},
    'loan28': {'businessSum': '370000', 'businessTerm': '24', 'defaultDueDay': '02'},
    'loan29': {'businessSum': '380000', 'businessTerm': '24', 'defaultDueDay': '02'},
    'loan30': {'businessSum': '390000', 'businessTerm': '12', 'defaultDueDay': '02'}}

def runFlowDay(flow):
    global dataList
    if not model:
        dataList,flow = getBatchInfo()
    # print(flow)
    logging.info("datalist流水图:" + str(dataList))
    logging.info("flow流水图:" + str(flow))
    # input()
    # sendRequest.isCleanDatabases()
    # fileOpt.cleanDirectionary(properties.basePath)
    # 清库
    cleanbatch()
    clean_db()
    lastDate = min(flow.keys())
    initBusinessDate(lastDate)
    syndcs = getSyndsByOrgid()
    # dbopera = Dboperator()
    # sql = "update " + cal_db + ".system_setup set business_date = '" + lastDate + "', batch_date = '" + lastDate + "'";
    # logging.debug("切日sql:" + sql)
    # dbopera.update(sql)
    # lastDate = ''
    for date in sorted(flow.keys()):
        logging.warning(date + '交易处理开始......')
        nowDate = datetime.datetime.strptime(date, "%Y-%m-%d")
        if lastDate != '':
            # days = (nowDate - lastDate).days
            runCommonInterface("endOfDayAllToDate", {"toBusinessDate": date, "accountingOrgNo": accountingOrgId})
            runModel(True)
        # for key, value in flow.get(date).items():
        if TractionType.putout in flow.get(date).keys():
            value = flow.get(date).get(TractionType.putout)
            for item in value:
                ele = dataList.get(item)
                ele["putoutDate"] = date
                ele["serialno"] = pouout(ele.copy())
                ele = dataList.get(item).copy()
                if ("syndicateSerialNo" not in ele.keys() or not ele["syndicateSerialNo"]) and syndcs:
                    for synd in syndcs:
                        ele["syndicateSerialNo"] = synd
                        ele["serialno"].append(pouout(ele.copy()))
        lastDate = nowDate
        # TractionTypes = flow.get(date)
        if TractionType.normalpayback in flow.get(date).keys():
            value = flow.get(date).get(TractionType.normalpayback)
            for loan, info in value.items():
                info["loanSerialNo"] = dataList.get(loan)["serialno"]
                info["businessDate"] = date
                info["transCode"] = "2001"
                info["paymentDate"] = date
                payback(info)
        if TractionType.prepayback in flow.get(date).keys():
            value = flow.get(date).get(TractionType.prepayback)
            for loan, info in value.items():
                info["loanSerialNo"] = dataList.get(loan)["serialno"]
                info["businessDate"] = date
                info["transCode"] = "2002"
                info["paymentDate"] = date
                payback(info)
    if model:
        saveBatchInfo(str(dataList), str(flow))
    # dbopera.conClose()
    # runTask(1)
    # fileOpt.closeCon()
    # sendRequest.closeCon()

def runFlowLoan(flow):
    samp = {}
    # logging.info(flow)
    # 获取 借据：动作  遍历
    # "loan1":{}
    for loan,action in flow.items():
        if loan not in dataList:
            dataList[loan] = {}
        # logging.debug("key:" + loan)
        # logging.debug("value:" + str(action))
        # 获取 日期：交易  遍历
        # "2018-02-27": {}
        for day,traction in action.items():
            if day not in samp:
                samp[day] = {}
            # logging.debug("key1:" + day)
            # logging.debug("value1:" + str(traction))
            # 遍历交易
            # TractionType.prepayback:{"prePayType": 3}
            for tname,param in traction.items():
                # logging.debug("tname:------" + str(tname))
                # logging.debug("tname + value :------" + str(traction.get(tname)))
                if TractionType.putout.equals(tname):
                    # print(samp)
                    if tname.name not in samp[day]:
                        # samp[day].update({tname.name:[]})
                        samp[day][tname]=[]
                    samp[day][tname].append(loan)
                    if traction[tname]:
                        # print(traction[tname])
                        # print(dataList[loan])
                        if dataList[loan]:
                            for key in traction[tname]:
                                dataList[loan][key] = traction[tname][key]
                        else:
                            dataList[loan] = traction[tname].copy()
                if TractionType.normalpayback.equals(tname) or TractionType.prepayback.equals(tname):
                    if tname.name not in samp[day]:
                        # samp[day].update({tname.name:[]})
                        samp[day][tname]={}
                    samp[day][tname][loan] = param
                    # samp[day][tname].append(loan)
    # print(dataList)
    # print(samp)
    runFlowDay(samp)

def runFlowExcel(filename):
    global dataList
    if not filename:
        filename = "../resource/测试场景.xlsx"
    dataList = getdatalistfromexcel(filename)
    flow = getscenefromexcel(filename)
    runFlowDay(flow)
    # pass

def putinto(key,origin,target):

    pass

# def runTask(self, days):
#     for i in range(days):
#         sendRequest.runTask()
#         if model == 1:
#             fileOpt.save()
#         elif model == 2:
#             fileOpt.check()

def temp(self):
    # sendRequest.payback(1,4000,1360.09)
    # sendRequest.payback(1,4400,1496.1,"test")
    # runTask(1)
    pass

def testday():
    samp = {
        "2018-02-15": {TractionType.putout: ["loan1", "loan2", "loan3", "loan4", "loan5", "loan6", "loan7", "loan8", "loan9", "loan10", "loan11", "loan12", "loan13", "loan14"]},
        # "2018-02-25": {TractionType.putout: ["loan15", "loan16", "loan17", "loan18"]},
        # "2018-02-26": {}
        "2018-02-25": {TractionType.putout: ["loan15", "loan16", "loan17", "loan18"], TractionType.prepayback: {"loan1": {"prePayType": 3}, "loan3": {"prePayType": 3}}},
        "2018-03-15": {TractionType.normalpayback: {"loan5": {"amt": 7000}}},
        "2018-03-17": {TractionType.normalpayback: {"loan6": {"amt": 8000}}},
        "2018-03-25": {TractionType.normalpayback: {"loan15": {"amt": 2000}}},
        "2018-04-15": {TractionType.prepayback: {"loan16": {"prePayType": 3}, "loan5": {"prePayType": 3}}},
        "2018-04-17": {TractionType.prepayback: {"loan7": {"prePayType": 3}, "loan17": {"prePayType": 3}}},
        "2018-04-25": {TractionType.normalpayback: {"loan15": {"amt": 2000}}, TractionType.prepayback: {"loan2": {"prePayType": 3}, "loan4": {"prePayType": 3}}},
        "2018-04-27": {TractionType.prepayback: {"loan15": {"prePayType": 3}, "loan8": {"prePayType": 3}}},
        "2018-05-15": {TractionType.prepayback: {"loan16": {"prePayType": 3}, "loan5": {"prePayType": 3}, "loan9": {"prePayType": 3}}},
        "2018-05-17": {TractionType.prepayback: {"loan7": {"prePayType": 3}}},
        "2018-05-25": {TractionType.prepayback: {"loan6": {"prePayType": 3}, "loan18": {"prePayType": 3}}},
        "2018-06-15": {TractionType.prepayback: {"loan16": {"prePayType": 3}}},
        "2018-06-17": {TractionType.prepayback: {"loan10": {"prePayType": 3}, "loan12": {"prePayType": 3}, "loan14": {"prePayType": 3}}},
        "2018-07-15": {TractionType.normalpayback: {"loan11": {"amt": 15000}, "loan13": {"amt": 17000}}},
        "2018-07-17": {TractionType.prepayback: {"loan11": {"prePayType": 3}}},
        "2018-07-30": {TractionType.prepayback: {"loan13": {"prePayType": 3}}},
        "2018-07-31":{}
    }

    runFlowDay(samp)

def testloan():
    samp = {
        # "loan1":{"2018-02-27": {TractionType.putout:{}, TractionType.prepayback:{"prePayType": 3}}},
        # "loan2":{"2018-02-28": {TractionType.putout:{}}, "2018-03-14": {TractionType.prepayback:{"prePayType": 3}}},
        # "loan3":{"2018-02-27": {TractionType.putout:{}}, "2018-03-15": {TractionType.prepayback:{"prePayType": 3}}},
        # "loan4":{"2018-03-06": {TractionType.putout:{}}, "2018-04-14": {TractionType.prepayback:{"prePayType": 3}}},
        # "loan5":{"2018-02-28": {TractionType.putout:{}}, "2018-03-28": {TractionType.normalpayback: {"amt": 0}}, "2018-04-28":{TractionType.normalpayback: {"amt": 0}}, "2018-05-28": {TractionType.normalpayback: {"amt": 0}}},
        # "loan5":{"2018-02-28": {TractionType.putout:{'defaultDueDay': '28'}}, "2018-03-29": {}},
        "loan5":{"2018-02-28": {TractionType.putout:{'defaultDueDay': '28'}}}
    }
    runFlowLoan(samp)

def test():
    samp = {
        '2018-01-31': {TractionType.putout: ['loan1', 'loan2', 'loan3']},
        '2018-02-01': {TractionType.prepayback: {'loan3': {'prePayType': 3}}},
        '2018-02-02': {
            TractionType.putout: ['loan4', 'loan6', 'loan8', 'loan9', 'loan11', 'loan12', 'loan13', 'loan14', 'loan15', 'loan16', 'loan17', 'loan18', 'loan19', 'loan20', 'loan21',
                                  'loan22', 'loan23', 'loan24', 'loan25', 'loan26', 'loan27', 'loan28', 'loan29']},
        '2018-02-12': {TractionType.putout: ['loan5', 'loan7', 'loan10', 'loan30']},
        '2018-03-02': {TractionType.normalpayback: {'loan8': {'amt': 0}}},
        '2018-03-04': {TractionType.normalpayback: {'loan9': {'amt': 0}}},
        '2018-03-12': {TractionType.normalpayback: {'loan5': {'amt': 0}, 'loan29': {'amt': 0}}},
        '2018-04-02': {TractionType.normalpayback: {'loan7': {'amt': 0}, 'loan8': {'amt': 0}, 'loan29': {'amt': 0}}, TractionType.prepayback: {'loan6': {'prePayType': 3}}},
        '2018-04-04': {TractionType.prepayback: {'loan10': {'prePayType': 3}, 'loan29': {'prePayType': 3}}},
        '2018-04-12': {TractionType.normalpayback: {'loan15': {'amt': 0}}},
        '2018-04-15': {TractionType.normalpayback: {'loan15': {'amt': 0}}, TractionType.prepayback: {'loan11': {'prePayType': 3}}},
        '2018-05-02': {TractionType.normalpayback: {'loan5': {'amt': 0}, 'loan7': {'amt': 0}, 'loan8': {'amt': 0}, 'loan15': {'amt': 0}},
                       TractionType.prepayback: {'loan12': {'prePayType': 3}, 'loan30': {'prePayType': 3}}},
        '2018-05-04': {TractionType.normalpayback: {'loan9': {'amt': 0}, 'loan15': {'amt': 0}}, TractionType.prepayback: {'loan5': {'prePayType': 3}}},
        '2018-05-12': {TractionType.prepayback: {'loan15': {'prePayType': 3}}},
        '2018-06-02': {TractionType.normalpayback: {'loan7': {'amt': 0}}},
        '2018-06-05': {
            TractionType.normalpayback: {'loan13': {'amt': 0}, 'loan14': {'amt': 0}, 'loan16': {'amt': 0}, 'loan17': {'amt': 0}, 'loan18': {'amt': 0}, 'loan19': {'amt': 0},
                                         'loan20': {'amt': 0}, 'loan21': {'amt': 0}, 'loan22': {'amt': 0}, 'loan23': {'amt': 0}, 'loan26': {'amt': 0}, 'loan27': {'amt': 0}},
            TractionType.prepayback: {'loan24': {'prePayType': 3}, 'loan28': {'prePayType': 3}}},
        '2018-06-07': {TractionType.normalpayback: {'loan14': {'amt': 0}, 'loan17': {'amt': 0}, 'loan19': {'amt': 0}, 'loan21': {'amt': 0}, 'loan23': {'amt': 0}}},
        '2018-06-09': {TractionType.normalpayback: {'loan14': {'amt': 0}, 'loan17': {'amt': 0}, 'loan19': {'amt': 0}, 'loan21': {'amt': 0}, 'loan23': {'amt': 0}},
                       TractionType.prepayback: {'loan26': {'prePayType': 3}, 'loan27': {'prePayType': 3}}},
        '2018-06-11': {TractionType.normalpayback: {'loan14': {'amt': 0}, 'loan17': {'amt': 0}, 'loan19': {'amt': 0}, 'loan21': {'amt': 0}, 'loan23': {'amt': 0}}},
        '2018-06-13': {TractionType.normalpayback: {'loan14': {'amt': 0}, 'loan17': {'amt': 0}, 'loan19': {'amt': 0}, 'loan21': {'amt': 0}, 'loan23': {'amt': 0}}},
        '2018-06-15': {TractionType.normalpayback: {'loan1': {'amt': 0}},
                       TractionType.prepayback: {'loan2': {'prePayType': 3}, 'loan14': {'prePayType': 3}, 'loan17': {'prePayType': 3}, 'loan19': {'prePayType': 3},
                                                 'loan21': {'prePayType': 3}, 'loan23': {'prePayType': 3}}},
        '2018-07-03': {TractionType.normalpayback: {'loan25': {'amt': 0}}}
    }
    runFlowDay(samp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, format='%(levelname)s-%(thread)d:%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d]: %(message)s')  # 设置日志级别
    # testday()
    # testday()
    # runFlowExcel("../resource/测试场景.xlsx")
    test()

