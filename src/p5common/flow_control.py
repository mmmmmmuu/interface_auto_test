import logging
import threading
from copy import copy

from p0constants.base_constants import THREADNUM
from p2myconfig.config import *
# 将主库数据保存至测试库
from p3db.Dboperator import Dboperator

sem = threading.Semaphore(THREADNUM)

def runModel(batch_no, model):
    '''
    :param model: bool true:保存   false：比较
    :return:
    '''
    testdb = Dboperator.getInstance(db_config=test_db)
    schemas = testdb.getAll(sql="select distinct table_schema from table_config where status = 1 order by sort_no;")
    threads = []
    method = {"record": _saveData, "check": _compareData}[model]
    product_db_config = copy(product_db)
    for schema in schemas:
        result = testdb.getAll(sql="select * from table_config where status = 1 and table_schema = %s order by sort_no;", param=schema["table_schema"])
        product_db_config["db"] = db_ref[schema["table_schema"]]
        productdb = Dboperator.getInstance(db_config=product_db_config)
        with sem:
            for setting in result:
                thread = threading.Thread(target=method, args=(setting, productdb, testdb, batch_no, sign))
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
    for thread in threads:
        thread.join()


def _saveData(info, productdb, testdb, batch_no, sign):
    totable = info["test_table"]
    logging.info(info["table_name"] + " --> " + str(threading.get_ident()) + " --> " + threading.currentThread().getName())
    if info["amount"] > 1:
        tablename = info["table_name"] + "_0"
        tables = [info["table_name"] + "_" + str(i) for i in range(info["amount"])]
    else:
        tablename = info["table_name"]
        tables = [tablename]
    stru = productdb.getAll(sql="desc %s;" % tablename)
    columns = "sign,batch_no," + ",".join([ele["Field"] for ele in stru])
    common = "%s" + ",%s" * (len(stru) + 1)
    num = 0
    for table in tables:
        logging.debug("开始处理 %s 表！" % table)
        datas = productdb.getAll(sql="select %s sign,'" + batch_no + " batch_no ',al.* from " + table + " al;", param=sign)
        valueList = []
        if datas:
            for data in datas:
                valueList.append([value for value in data.values()])
            num = testdb.insertMany("insert into " + totable + " (" + columns + ") values(" + common + ")", valueList)
    logging.debug("表" + tablename + "共插入" + str(num) + "条数据！")
    return num


def _compareData(info, productdb, testdb, sign):
    # print(info)
    tablename = info["table_name"]
    totable = info["test_table"]
    cols = info["columns"].replace(" ", "").split(",")
    print(tablename + " --> " + str(threading.get_ident()) + " --> " + threading.currentThread().getName())
    olddata = productdb.getAll("desc acct_loan;")
    columns = [ele["Field"] for ele in olddata]
    old = []
    test = []
    num = 0
    for odata in "olddatas":
        tmp = {}
        for col in cols:
            tmp[col] = odata[col]
        old.append(tmp)
    for testdata in "testdatas":
        tmp = {}
        for col in cols:
            tmp[col] = testdata[col]
        test.append(tmp)
    for ele in old:
        num += 1
        if not ele in test:
            print(num)
            print(test)
            raise Exception(str(ele) + "数据找不到")
    logging.info("表" + tablename + "共比较" + str(num) + "条数据！")


def saveBatchInfo(dataList, flow):
    sql = 'insert into batch_info (batch_no,data_list,flow_day,prefix,suffix,create_date) values(%s,%s,%s,curdate()) ' \
          'on DUPLICATE key update data_list="%s",flow_day="%s";'
    dbopr = Dboperator.getInstance("test")
    # print(dataList)
    # print(flow)
    dbopr.insert(sql=sql, param=(batch_no, dataList, flow, dataList, flow))
    dbopr.end()
    dbopr.dispose()


def getBatchInfo():
    sql = 'select data_list,flow_day from batch_info where batch_no = %s;';
    dbopr = Dboperator.getInstance("test")
    result = dbopr.getOne(sql=sql, param=(batch_no,))
    return result


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    runModel("dfghjkl;/")