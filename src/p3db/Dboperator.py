#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from p2myconfig.config import product_db


class Dboperator():

    # 数据库连接实例列表
    _dbinstances = {}

    @classmethod
    def getInstance(self, db_config=None):
        assert db_config, "数据库配置为空"
        dbstr = db_config["host"] + str(db_config["port"]) + db_config["db"]
        if dbstr not in self._dbinstances.keys():
            self._dbinstances[dbstr] = Dboper(db_config=db_config)
        return self._dbinstances[dbstr]

def conn(func):
    def wrapper(*args, **kwargs):
        conn = None
        if "cursor" not in kwargs.keys():
            conn = args[0].getConn()
            cursor = conn.cursor()
            kwargs["cursor"] = cursor
        result = func(*args, **kwargs)
        if conn:
            conn.commit()
            conn.close()
        return result
    return wrapper


class Dboper():
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self, db_config=product_db):
        self._pool = PooledDB(creator=pymysql,
                              cursorclass=DictCursor,
                              **db_config
                              )

    def getConn(self):
        return self._pool.connection()

    @conn
    def getAll(self, sql, param=None, cursor=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchall()
        else:
            result = False
        return result

    @conn
    def getOne(self, sql, param=None, cursor=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        logging.debug("sql: " + sql)
        logging.debug(param)
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchone()
        else:
            result = False
        return result

    @conn
    def getMany(self, sql, num=None, param=None, cursor=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchmany(num)
        else:
            result = False
        return result

    @conn
    def insertMany(self, sql, values,cursor=None):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = cursor.executemany(sql, values)
        return count

    @conn
    def __query(self, sql, param=None, cursor=None):
        # print(threading.get_ident())
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        return count

    @conn
    def update(self, sql, param=None, cursor=None):
        logging.debug(sql)
        logging.debug(param)
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param, cursor=cursor)

    @conn
    def updateMany(self, sqlinfo, cursor=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        num = 0
        for item in sqlinfo:
            num += self.__query(sql=item[0], param=item[1], cursor=cursor)
        return num

    @conn
    def insert(self, sql, param=None, cursor=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param, cursor=cursor)

    @conn
    def delete(self, sql, param=None, cursor=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param, cursor=cursor)

    def getInsertId(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        conn = self.getConn()
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        result = None
        if count == 1:
            result = cursor._result.insert_id
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def begin(self, conn):
        """
        @summary: 开启事务
        """
        conn.autocommit(0)

    def end(self, conn, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            conn.commit()
        else:
            conn.rollback()

    @conn
    def test(self, sql, cursor=None):
        cursor.execute("select * from acct_loan;")
        return cursor.fetchall()

if __name__ == '__main__':
    mysql = Dboperator.getInstance()
    # result = mysql.getOne("select * from system_setup;")
    result = mysql.test(sql='')
    print(result)
