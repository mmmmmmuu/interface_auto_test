import datetime
from json import JSONDecodeError

import requests

from p2myconfig.config import HEADERS, product_db
from p4dao.dbDao import getInterfaceInfo, initBusinessDate, BATCH_INTERFACE, get_user_batch_env
from p3db.Dboperator import Dboperator
from p5common.common import common_utils
from p8executor.baseRunner import BaseRunner
from p6decorate.Decorate import *
from p5common.flow_control import runModel
from p5common.tempVariable import TempVariable
from p5common.utils import iter_replace, replace


class CommonInterface(BaseRunner):

    def __init__(self, batch_no, interface_info=None, interface_id=None, alias=None, parent_id=None, params=None, tranname="", loc=""):
        BaseRunner.__init__(self, batch_no=batch_no, info=interface_info, id=interface_id, alias=alias, parent_id=parent_id, type=BATCH_INTERFACE,
                            params=params, tranname=tranname)
        if not self._info:
            self._info = getInterfaceInfo(id=self._id, alias=self._alias)
        if not self._alias:
            self._alias = self._info["alias"]
        if not self._tranname:
            self._tranname = self._info["alias"]
        self._task_name = self._info["alias"]
        self._loc = loc
        self._url = "/".join([TempVariable.getValue("{sda_url}", batch_no), self._info["service_name"].lower(), self._info["method_name"]])
        TempVariable.initResp(loc=self._loc)

    def _preaction(self):
        super()._preaction()
        dbopr = Dboperator.getInstance(db_config=replace(copy(product_db), {"db": "calculator_xfm_lhd"}))
        business_date = dbopr.getOne("select business_date from system_setup;")["business_date"].strftime("%Y-%m-%d")
        TempVariable.saveAction(value={"businessDate": business_date}, loc=self._loc)

    def _dealParams(self):
        super()._dealParams()
        # TempVariable.addToBatch(self._params, batch_no=self._batch_no)
        inter = json.loads(self._info["request_param"])
        if self._tranname:
            self._tranname = self._info["desc"].format(self._tranname)
        else:
            self._tranname = self._info["desc"]
        params = iter_replace(inter, self._params, loc=self._loc)
        self._params = params
        # TempVariable.addToBatch(self._params, batch_no=self._batch_no)

    def _dobefore(self):
        super()._dobefore()
        logging.info(self._tranname + "接口请求地址：" + self._url)
        logging.info(self._tranname + "接口参数：" + str(self._params))
        if "putoutDate" in self._params.keys():
            initBusinessDate(cal_db="calculator_xfm_lhd", business_date=self._params["putoutDate"])

    def _run(self):
        '''
        :param iname: 接口名称 str
        :param info: 参数 dict
        :param flag: bool  是否检查返回状态和result  true：是 false 否
        :param tranName: 日志前置
        :return: 接口请求结果
        '''
        super()._run()
        rev = requests.post(url=self._url, data=json.dumps(self._params), headers=HEADERS)
        self._response = rev

    def _response_check(self):
        status, msg = super()._response_check()
        if not status:
            return status, msg
        if self._response.status_code != 200:
            return False, self._task_name + "接口返回状态为" + str(self._response.status_code) + ", 状态检查失败!"
        self._response = self._response.content.decode("utf8")
        return True, ""

    def _dealResponse(self):
        super()._dealResponse()
        try:
            self._response = json.loads(self._response)
        except JSONDecodeError as e:
            # traceback.print_exc()
            pass

# 获取系统日期
def getBusinessDate():
    info = {
        "productNo": 5003,
        "accountingOrgNo": 10081001
    }
    iname = "queryBusinessDate"
    logging.debug("查询核算业务日期请求地址：" + "http://10.1.81.7:25555/hcfc-core-calculator/" + iname)
    logging.debug("查询核算业务日期接口请求参数：" + str(info))
    try:
        rev = requests.post(url="http://10.1.81.7:25555/hcfc-core-calculator/" + iname, data=json.dumps(info), headers=HEADERS)
    except Exception as e:
        logging.error(iname + "接口调用失败")
        raise RuntimeError()
    logging.debug(iname + "接口返回结果：" + str(rev.content.decode("utf-8")))
    return '-'.join(["%02d" % i for i in json.loads(rev.content.decode("utf-8"))["businessDate"]])


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET,
                        format='%(levelname)s-%(thread)d:%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d]: %(message)s')  # 设置日志级别
    # getBusinessDate()
    batch_no = "111111111"
    TempVariable.addToBatch(get_user_batch_env(1, 1), batch_no)
    print(TempVariable.getValue("sda_url"))
    CommonInterface(batch_no=batch_no, interface_id=1, parent_id=0, loc=batch_no).execute()

