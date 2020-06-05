from p0constants.batch_constants import *
from p3db.Dboperator import Dboperator
from p2myconfig.config import test_db, product_db


def getInterfaceGroupInfo(id=None, alias=None):
    condtions = []
    params = []
    if id:
        condtions.append(" id=%s ")
        params.append(id)
    if alias:
        condtions.append(" alias=%s ")
        params.append(alias)
    dbopr = Dboperator().getInstance(db_config=test_db)
    return dbopr.getOne('''select * from interface_group_info  where %s ''' % " and ".join(condtions), params)

def getInterByGroup(id=None, alias=None):
    condtions = []
    params = []
    if id:
        condtions.append(" ig.id=%s ")
        params.append(id)
    if alias:
        condtions.append(" ig.alias=%s ")
        params.append(alias)
    dbopr = Dboperator().getInstance(db_config=test_db)
    return dbopr.getAll('''select ig.alias group_alias, ibi.* from interface_group_info ig
                        inner join group_interface_mapping gim on ig.id=gim.group_id
                        inner join interface_info ibi on gim.interface_id=ibi.id
                        where %s order by `order` ''' % " and ".join(condtions), params)

def getInterfaceInfo(id=None, alias=None):
    condtions = []
    params = []
    if id:
        condtions.append(" id=%s ")
        params.append(id)
    if alias:
        condtions.append(" alias=%s ")
        params.append(alias)
    dbopr = Dboperator().getInstance(db_config=test_db)
    return dbopr.getOne(''' select * from interface_info where ''' + " and ".join(condtions), params)


def getBatchInfo(id):
    dbopr = Dboperator().getInstance(db_config=test_db)
    return dbopr.getOne(''' select * from batch_info where id=%s''', id)


def getInterByBatch(id):
    dbopr = Dboperator().getInstance(db_config=test_db)
    return dbopr.getAll(''' select * from batch_interface_mapping where batch_id=%s order by `order` ''', id)

# 初始化日期
def initBusinessDate(cal_db, business_date, batch_date=None, book_date=None):
    batch_date = batch_date if batch_date else business_date
    book_date = book_date if book_date else business_date
    dboperate = Dboperator.getInstance(db_config=product_db)
    sql = "update " + cal_db + ".system_setup set business_date='" + business_date + "',batch_date='" + batch_date + "',book_date='" + book_date + "';"
    dboperate.update(sql)
    dboperate.update("truncate table bat_task_log;")


def getAllInterfaceInfos():
    dbopr = Dboperator().getInstance(db_config=test_db)
    return dbopr.getAll(''' select * from interface_info where status=1 ''')


def getTaskInfo(type, id):
    dbopr = Dboperator().getInstance(db_config=test_db)
    if type == BATCH_BATCH:
        table = "batch_info"
    elif type == BATCH_GROUP:
        table = "interface_group_info"
    elif type == BATCH_INTERFACE:
        table = "interface_info"
    return dbopr.getOne("select * from " + table + " where id=%s;", id)

def get_user_batch_env(user_id, batch_id):
    dbopr = Dboperator().getInstance(db_config=test_db)
    records = dbopr.getAll("select `key`, `value` from envirnment where creater=%s and (batch_id=%s or batch_id=0) order by batch_id asc", param=(user_id, batch_id))
    result = {}
    for item in records:
        result[item["key"]] = item["value"]
    return result

def get_plugins(batch_id):
    dbopr = Dboperator().getInstance(db_config=test_db)
    records = dbopr.getAll("select pi.* from batch_plugins_mapping bpm inner join plugin_info pi on bpm.plugin_id=pi.id where bpm.batch_id=%s order by pi.`order`;", param=(batch_id,))
    return records

if __name__ == '__main__':
    result = get_user_batch_env(1, 1)
    print(result)
