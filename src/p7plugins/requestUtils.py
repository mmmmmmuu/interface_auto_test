import json
import logging

from p3db.Dboperator import Dboperator
from p2myconfig.config import test_db
from p5common.baseMethod import baseMethod

class requestUtils(baseMethod):

    def __init__(self, instance):
        self._task_id = instance._task_id
        self._batch_no = instance._batch_no
        self._id = ""
        self._dbopr = Dboperator.getInstance(db_config=test_db)

    def _saveParams(self, **kwargs):
        instance = kwargs["instance"]
        param = instance._params
        if param and isinstance(param, dict):
            param = json.dumps(param)
        self._id = self._dbopr.getInsertId("INSERT INTO `request_log`(`batch_no`, `task_id`, `times`, `request_arg`, `response_arg`, `create_time`)\
                                       VALUES (%s,%s,(select times from run_batch_log where id=%s),%s,null,now())", (self._batch_no, self._task_id, self._task_id, param))

    def _saveResponse(self, **kwargs):
        instance = kwargs["instance"]
        response = instance._response
        if response and isinstance(response, dict):
            response = json.dumps(response)
        assert self._id, "request_log请先初始化入参。。"
        self._dbopr.update("update request_log set response_arg=%s where id=%s", (response, self._id))

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    # utils = RequestUtils(batch_no=1, task_id=20)
    # utils.saveParam({"a":1, 'b':2})
    # utils.updateResponse({1: 'a', 2: "b"})
