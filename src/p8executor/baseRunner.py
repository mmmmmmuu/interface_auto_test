import traceback

from p0constants.batch_constants import BATCH_INTERFACE
from p5common.common import common_utils
from p6decorate.Decorate import *
from p0constants.task_constants import *
from p5common.tempVariable import TempVariable
from p5common.baseMethod import baseMethod


class BaseRunner(baseMethod):

    def __init__(self, batch_no, info=None, id=None, alias=None, mapping_id=None, parent_task_id=None, type=BATCH_INTERFACE, params=None, tranname=""):
        self._batch_no = batch_no
        self._info = info
        self._id = id
        self._alias = alias
        self._params = params if params else {}
        self._tranname = tranname
        self._response = {}
        self._status = 1
        self._task_name = ""
        self._loc = ""
        self._mapping_id = mapping_id
        self._parent_task_id = parent_task_id
        self._type = type
        self._task_id = None
        self._task = None
        self._request_utils = None

    def _skipcheck(self):
        self._cutil = common_utils(self)
        status, msg = self._cutil.runPlugins(type=self._type, method="_skipcheck", check_type=2, instance=self)
        if not status:
            return RUNNING_FAIL, msg
        return RUNNING_SUCCESS, ""

    def _exitcheck(self):
        status, msg = self._cutil.runPlugins(type=self._type, method="_exitcheck", check_type=2, instance=self)
        if not status:
            return RUNNING_FAIL, msg
        return RUNNING_SUCCESS, ""

    # 替换变量
    def _dealParams(self):
        self._cutil.runPlugins(type=self._type, method="_dealParams", check_type=1, instance=self)


    # 保存变量
    def _saveParams(self):
        self._cutil.runPlugins(type=self._type, method="_saveParams", check_type=1, instance=self)
        TempVariable.saveParam(value=self._params, loc=self._loc)

    # 执行前做 如打印执行日志
    def _dobefore(self):
        self._cutil.runPlugins(type=self._type, method="_dobefore", check_type=1, instance=self)


    # 执行自定义动作
    def _preaction(self):
        self._cutil.runPlugins(type=self._type, method="_preaction", check_type=1, instance=self)


    # 执行
    def _run(self):
        return self._cutil.runPlugins(type=self._type, method="_run", check_type=1, instance=self)


    # 返回结果检查
    def _response_check(self):
        status, msg = self._cutil.runPlugins(type=self._type, method="_response_check", check_type=2, instance=self)
        if not status:
            return RUNNING_FAIL, msg
        return RUNNING_SUCCESS, ""

    # 处理返回
    def _dealResponse(self):
        self._cutil.runPlugins(type=self._type, method="_dealResponse", check_type=1, instance=self)


    # 讲执行结果保存到内存供后续引用
    def _saveResponse(self):
        self._cutil.runPlugins(type=self._type, method="_saveResponse", check_type=1, instance=self)
        TempVariable.saveResponse(value=self._response, loc=self._loc)
        # self._request_utils.updateResponse(self._response)


    # 执行自定义后置动作
    def _ateraction(self):
        self._cutil.runPlugins(type=self._type, method="_ateraction", check_type=1, instance=self)

    # 执行后操作 如打印日志
    def _doafter(self):
        self._cutil.runPlugins(type=self._type, method="_doafter", check_type=1, instance=self)
        # self._task.updateTaskStatus(self._status)
        logging.info(self._tranname + "接口返回结果为：" + str(self._response))


    # 流程定义，主要执行方法
    def execute(self):
        status, msg = self._skipcheck()
        if status != RUNNING_SUCCESS:
            return RUNNING_SKIP, msg
        status, msg = self._exitcheck()
        if status != RUNNING_SUCCESS:
            self._status = TASK_FAIL
            self._doafter()
            return RUNNING_EXIT, msg
        self._preaction()
        self._dealParams()
        self._dobefore()
        self._saveParams()
        try:
            status, response = self._run()
            if status != RUNNING_SUCCESS:
                self._status = TASK_FAIL
                self._doafter()
                return status, response
        except Exception as e:
            traceback.print_exc()
            self._status = TASK_ERROR
            self._doafter()
            return RUNNING_ERROR, e
        status, msg = self._response_check()
        if status != RUNNING_SUCCESS:
            self._status = TASK_FAIL
            self._doafter()
            return status, msg
        self._status = TASK_SUCCESS
        self._dealResponse()
        self._saveResponse()
        self._ateraction()
        self._doafter()
        return RUNNING_SUCCESS, self._response
