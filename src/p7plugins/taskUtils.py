
import logging
from p0constants.task_constants import *
from p0constants.batch_constants import *
from p4dao.dbDao import getTaskInfo
from p3db.Dboperator import Dboperator
from p2myconfig.config import test_db
from p5common.baseMethod import baseMethod


class taskUtils(baseMethod):

    def __init__(self, **kwargs):
        self._dbopr = Dboperator.getInstance(db_config=test_db)

    def _skipcheck(self, **kwargs):
        instance = kwargs["instance"]
        condtions = []
        params = []
        if instance._batch_no:
            condtions.append(" batch_no=%s ")
            params.append(instance._batch_no)
        if instance._mapping_id:
            condtions.append(" mapping_id=%s ")
            params.append(instance._mapping_id)
        if instance._parent_task_id:
            condtions.append(" parent_id=%s ")
            params.append(instance._parent_task_id)
        if instance._type:
            condtions.append(" type=%s ")
            params.append(instance._type)
        batch_tasks = self._dbopr.getAll("select * from run_batch_log where " + " and ".join(condtions), param=params)
        if not batch_tasks:
            return True, ""
        assert len(batch_tasks) <= 1, "同一batch存在满足条件的多条记录"
        instance._task_id = batch_tasks[0]["id"]
        task_name = getTaskInfo(type=instance._type, id=instance._mapping_id)[
            {BATCH_INTERFACE: "interface_name", BATCH_GROUP: "group_name", BATCH_BATCH: "batch_name"}[instance._type]]
        assert batch_tasks[0]["status"] != TASK_RUNNING, ("%s正在执行，程序退出，请稍后再试！" % task_name)
        if batch_tasks[0]["status"] == TASK_SUCCESS:
            logging.warning("%s已经执行成功，跳过！" % task_name)
            return False, "%s已经执行成功，跳过！" % task_name
        elif batch_tasks[0]["status"] == TASK_FAIL:
            return True, ""

    def _saveParams(self, **kwargs):
        instance = kwargs["instance"]
        if instance._task_id:
            self._dbopr.update("update run_batch_log set status=1,times=times+1,start_time=now(),end_time=null where id=%s;", instance._task_id)
        else:
            instance._task_id = self._dbopr.getInsertId(
                """ insert into run_batch_log (`batch_no`, `mapping_id`, `type`, `parent_id`, `times`, `status`, `creater`, `start_time`)
                 values(%s,%s,%s,%s,%s,%s,%s,now()) """,
                (instance._batch_no, instance._mapping_id, instance._type, instance._parent_task_id, 1, TASK_RUNNING, 1))
        return instance._task_id

    def _doafter(self, **kwargs):
        instance = kwargs["instance"]
        self._dbopr.update("update run_batch_log set status=%s, end_time=now() where id=%s;", (instance._status, instance._task_id))

    # def setId(self, id):
    #     self._id=id

# if __name__ == '__main__':
#     task = TaskUtils(batch_no="1123", mapping_id=1, parent_id=2, type=BATCH_INTERFACE)
#     result = task.isTaskCanRun()
#     task.setId(20)
#     result1 = task.initTask()
    # task.updateTaskStatus(5)
    # a = 1

