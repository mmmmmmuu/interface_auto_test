
import logging
from p0constants.task_constants import *
from p0constants.batch_constants import *
from p4dao.dbDao import getTaskInfo
from p3db.Dboperator import Dboperator
from p2myconfig.config import test_db
from p5common.baseMethod import baseMethod


class taskUtils(baseMethod):

    def __init__(self, instance):
        self._batch_no = instance._batch_no
        self._mapping_id = instance._mapping_id
        self._parent_id = instance._parent_id
        self._type = instance._type
        self._dbopr = Dboperator.getInstance(db_config=test_db)
        self._id = None
        self._status = instance._status

    def _skipcheck(self, **kwargs):
        condtions = []
        params = []
        instance = kwargs["instance"]
        if self._batch_no:
            condtions.append(" batch_no=%s ")
            params.append(self._batch_no)
        if self._mapping_id:
            condtions.append(" mapping_id=%s ")
            params.append(self._mapping_id)
        if self._parent_id:
            condtions.append(" parent_id=%s ")
            params.append(self._parent_id)
        if self._type:
            condtions.append(" type=%s ")
            params.append(self._type)
        batch_tasks = self._dbopr.getAll("select * from run_batch_log where " + " and ".join(condtions), param=params)
        if not batch_tasks:
            return True
        assert len(batch_tasks) <= 1, "同一batch存在满足条件的多条记录"
        self._id = batch_tasks[0]["id"]
        instance._id = self._id
        task_name = getTaskInfo(type=self._type, id=self._mapping_id)[
            {BATCH_INTERFACE: "interface_name", BATCH_GROUP: "group_name", BATCH_BATCH: "batch_name"}[self._type]]
        assert batch_tasks[0]["status"] != TASK_RUNNING, ("%s正在执行，程序退出，请稍后再试！" % task_name)
        if batch_tasks[0]["status"] == TASK_SUCCESS:
            logging.warning("%s已经执行成功，跳过！" % task_name)
            return False
        elif batch_tasks[0]["status"] == TASK_FAIL:
            return True

    def _dobefore(self, **kwargs):
        if self._id:
            self._dbopr.update("update run_batch_log set status=1,times=times+1,start_time=now(),end_time=null where id=%s;", self._id)
        else:
            self._id = self._dbopr.getInsertId(
                """ insert into run_batch_log (`batch_no`, `mapping_id`, `type`, `parent_id`, `times`, `status`, `creater`, `start_time`)
                 values(%s,%s,%s,%s,%s,%s,%s,now()) """,
                (self._batch_no, self._mapping_id, self._type, self._parent_id, 1, TASK_RUNNING, 1))
        return self._id

    def _doafter(self, **kwargs):
        self._dbopr.update("update run_batch_log set status=%s, end_time=now() where id=%s;", (self._status, self._id))

    # def setId(self, id):
    #     self._id=id

if __name__ == '__main__':
    task = TaskUtils(batch_no="1123", mapping_id=1, parent_id=2, type=BATCH_INTERFACE)
    result = task.isTaskCanRun()
    task.setId(20)
    result1 = task.initTask()
    # task.updateTaskStatus(5)
    # a = 1

