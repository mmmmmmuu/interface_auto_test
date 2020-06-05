import json
from copy import copy

from p4dao.dbDao import getInterByGroup, getInterfaceInfo, getInterfaceGroupInfo, BATCH_GROUP
from p5common.common import common_utils
from p8executor.InterfaceRunner import CommonInterface
from p8executor.baseRunner import BaseRunner
from p5common.tempVariable import TempVariable
from p5common.utils import iter_replace


class InterfaceGroup(BaseRunner):

    def __init__(self, batch_no, group_info=None, group_id=None, alias=None, parent_id=None, params=None, tranname="", loc=""):
        BaseRunner.__init__(self, batch_no=batch_no, info=group_info, id=group_id, alias=alias, parent_id=parent_id, type=BATCH_GROUP, params=params,
                            tranname=tranname)
        if not self._info:
            self._info = getInterfaceGroupInfo(id=self._id, alias=alias)
        self._task_name = self._info["alias"]
        if not self._tranname:
            self._tranname = self._info["alias"]
        self._alias = self._info["alias"]
        # self._loc = self._info["alias"] if not loc else (loc + "." + self._info["alias"])
        self._loc = loc
        TempVariable.initResp(loc=self._loc)

    def _dealParams(self):
        super()._dealParams()
        if self._info["request_param"]:
            param = json.loads(self._info["request_param"])
            param.update(self._params)
            self._params = param

    def _run(self):
        '''
        :param iname: 接口名称 str
        :param info: 参数 dict
        :param flag: bool  是否检查返回状态和result  true：是 false 否
        :param tranName: 日志前置
        :return: 接口请求结果
        '''
        super()._run()
        interfaces = getInterByGroup(id=self._info["id"])
        for inter in interfaces:
            response = CommonInterface(batch_no=self._batch_no, interface_info=inter, parent_id=self._task_id, params=copy(self._params),
                                       loc=self._loc + "." + inter["alias"]).execute()
            if response and isinstance(response, dict):
                self._response.update(response)
                TempVariable.saveResponse(value=self._response, loc=self._loc)
            # iter_replace(self._params, self._response)
        return self._response
