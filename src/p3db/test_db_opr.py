import json
import logging
from copy import copy

from p3db.Dboperator import Dboperator
from p2myconfig.config import test_db, product_db, cal_db, account_db, public_db
import pickle

def cleanbatch():
    logging.info('清空test库开始...')
    dbopr = Dboperator.getInstance(db_config=test_db)
    tables = [item["Tables_in_%s" % test_db["db"]] for item in dbopr.getAll("show full tables where Table_type='BASE TABLE';")]
    sqls = ['drop table %s;' % item["test_table"] for item in dbopr.getAll("select test_table from table_config") if item["test_table"] in tables]
    # print(sqls)
    for sql in sqls:
        logging.debug("开始执行sql: " + sql)
        dbopr.update(sql);
    logging.info('清空test库结束...')

def init_batch():
    logging.info("test数据库初始化开始")
    t_db = Dboperator.getInstance(db_config=test_db)
    schemas = t_db.getAll("select distinct table_schema from table_config where status = 1;")
    if not schemas:
        return
    product_dbs = {}
    db_config = copy(product_db)
    for schema in [item["table_schema"] for item in schemas]:
        db_config["db"] = {"calculator": cal_db, "account": account_db, "public": public_db}[schema]
        product_dbs[schema] = Dboperator.getInstance(db_config=db_config)
    tables = t_db.getAll("select id,table_name,table_schema,amount,test_table from table_config where status = 1")
    column_infos = []
    for table in tables:
        logging.debug("开始处理%s表" % table["table_name"])
        table_info = product_dbs[table["table_schema"]].getAll("desc %s;" % ((table["table_name"] + "_0") if table["amount"] > 1 else table["table_name"]))
        columns = [item["Field"] for item in table_info]
        column_infos += [(table["id"], table["table_schema"], table["table_name"], item["Field"], 0) for item in table_info \
                    if item["Field"] not in ["id", "create_time", "update_time"]]
        if table["amount"] > 1:
            table["table_name"] = table["table_name"] + "_0"
        create_sql = product_dbs[table["table_schema"]].getOne("show create table %s;" % table["table_name"])["Create Table"]
        create_sql = create_sql.replace("CREATE TABLE `%s` (" % table["table_name"], "CREATE TABLE `%s` (" % table["test_table"], 1).replace("AUTO_INCREMENT", "", 1)
        logging.debug(create_sql)
        t_db.update(create_sql)
        t_db.update("""ALTER TABLE {table_name} 
                        ADD COLUMN `index` int(0) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id' FIRST, 
                        ADD COLUMN `sign` varchar(63) NOT NULL COMMENT '唯一标识' AFTER `index`, 
                        ADD COLUMN `batch_no` varchar(63) NOT NULL COMMENT '批次号' AFTER `sign`, 
                        %s
                        DROP PRIMARY KEY, 
                        ADD PRIMARY KEY (`index`) USING BTREE;""".format(table_name=table["test_table"]) % ("MODIFY COLUMN `id` bigint(20) NOT NULL COMMENT 'id' AFTER `batch_no`," if "id" in columns else ""))
    logging.debug("开始初始化check_columns表")
    t_db.update("create table `check_columns_tmp` like `check_columns`;")
    # 更新 check_columns_tmp 检查字段为最新的
    t_db.insertMany("INSERT INTO `check_columns_tmp`(`table_config_id`, `table_schema`, `table_name`, `column_name`, `status`) VALUES (%s, %s, %s, %s, %s)", column_infos)
    t_db.update("delete from check_columns where (table_config_id, table_schema, table_name, column_name) not in (select table_config_id, table_schema, table_name, column_name from check_columns_tmp);")
    t_db.update("update check_columns col,check_columns_tmp col_tmp set col.table_schema=col_tmp.table_schema, col.table_name=col_tmp.table_name where col.table_config_id=col_tmp.table_config_id and col.column_name=col_tmp.column_name;")
    t_db.update("insert into check_columns (table_config_id, table_schema, table_name, column_name) select table_config_id, table_schema, table_name, column_name from check_columns_tmp where (table_config_id, column_name) not in (select table_config_id, column_name from check_columns);")
    t_db.delete("drop table `check_columns_tmp`;")
    logging.info("test数据库初始化完成")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    # cleanbatch()
    # init_batch()
    dbopr = Dboperator.getInstance(db_config=test_db)
    # for key, value in scene.items():
    #     dbopr.update('''INSERT INTO `test_calculator`.`request_params`(`service_name`, `method_name`, `request_type`, `desc`, `request_param`, `status`, `create_time`, `update_time`)
    #     VALUES ('HCFC-CORE-CALCULATOR', '%s', 'POST', '%s', '%s', 1, '2020-05-16 21:49:56', '2020-05-16 21:49:59');''' % (
    #     key, value["desc"], json.dumps(value["info"])))
    # print(type(pickle.dumps(scene["flexiblePutoutApply"]["info"])))
    # dbopr.update('''INSERT INTO `test_calculator`.`request_params`(`service_name`, `method_name`, `request_type`, `desc`, `request_param`, `status`, `create_time`, `update_time`)
    # VALUES ('HCFC-CORE-CALCULATOR', '%s', 'POST', '%s', %s, 1, '2020-05-16 21:49:56', '2020-05-16 21:49:59');''', (
    # "flexiblePutoutApply", scene["flexiblePutoutApply"]["desc"], pickle.dumps(scene["flexiblePutoutApply"]["info"])))
    # param = dbopr.getOne("select request_param from request_params where `method_name` = 'flexiblePutoutApply';")["request_param"]
    # print(json.loads(param)["rateList"][1]["businessRate"])
    init_batch()

