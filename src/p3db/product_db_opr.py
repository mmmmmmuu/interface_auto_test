
import pymysql
from p2myconfig.config import product_db
from copy import copy


def clean_db():
    for db in cal_db, account_db, public_db:
        db_config = copy(product_db)
        db_config.update({"db": db})
        connect = pymysql.Connect(cursorclass=pymysql.cursors.DictCursor, **db_config)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        cursor.execute("show full tables where Table_type='BASE TABLE';")
        table_list = cursor.fetchall()
        for table in table_list:
            if table["Tables_in_%s" % db] not in notCleanTable[db]:
                cursor.execute("truncate table %s;" % table["Tables_in_%s" % db])
                print("truncate table %s;" % table["Tables_in_%s" % db])
        cursor.close()
        connect.commit()
        print("---------------------------")
    cursor.close()
    connect.close()

