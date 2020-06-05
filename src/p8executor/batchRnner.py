from p0constants.task_constants import *
from p4dao.dbDao import getInterByGroup, getInterfaceInfo, getBatchInfo, getInterByBatch, BATCH_BATCH, get_user_batch_env, get_plugins
from p5common.common import common_utils
from p8executor.InterfaceRunner import CommonInterface
from p8executor.baseRunner import BaseRunner
from p6decorate.Decorate import *
from p8executor.interfaceGroupRunner import InterfaceGroup
from p5common.tempVariable import TempVariable


class Batch(BaseRunner):

    def __init__(self, batch_no, batch_info=None, batch_id=None, alias=None, params=None, tranname=""):
        BaseRunner.__init__(self, batch_no=batch_no, info=batch_info, id=batch_id, alias=alias, params=params, type=BATCH_BATCH, mapping_id=batch_id,
                            parent_task_id=0, tranname=tranname)
        if not self._info:
            self._info = getBatchInfo(id=self._id)
        self._task_name = self._info["alias"]
        if not self._tranname:
            self._tranname = self._info["batch_name"]
        self._alias = self._info["alias"]
        self._loc = self._batch_no
        TempVariable.initResp(loc=self._loc)
        TempVariable.addToBatch(get_user_batch_env(1, 1), batch_no)
        TempVariable.addToBatch({"plugins": get_plugins(self._info["id"])}, batch_no)

    def _run(self):
        '''
        :param iname: 接口名称 str
        :param info: 参数 dict
        :param flag: bool  是否检查返回状态和result  true：是 false 否
        :param tranName: 日志前置
        :return: 接口请求结果
        '''
        super()._run()
        interfaces = getInterByBatch(id=self._info["id"])
        for inter in interfaces:
            param = copy(self._params)
            tmp = {} if not inter["request_param"] else json.loads(inter["request_param"])
            param.update(tmp)
            if inter["interface_type"] == "interface":
                status, response = CommonInterface(batch_no=self._batch_no, interface_id=inter["interface_id"], mapping_id=inter["id"],
                                           parent_task_id=self._task_id, params=param, loc=self._loc + "." + inter["alias"]).execute()
            elif inter["interface_type"] == "group":
                status, response = InterfaceGroup(batch_no=self._batch_no, group_id=inter["interface_id"], mapping_id=inter["id"],
                                          parent_task_id=self._task_id, params=param, loc=self._loc + "." + inter["alias"]).execute()
            if response and isinstance(response, dict):
                self._response.update(response)
                TempVariable.saveResponse(value=self._response, loc=self._loc)
            if status == RUNNING_EXIT:
                self._status = 2
                return ""
            # self._params.update(self._response)
        return self._response


    def _doafter(self):
        super()._doafter()
        TempVariable.cleanBatch(batch_no=self._batch_no)

