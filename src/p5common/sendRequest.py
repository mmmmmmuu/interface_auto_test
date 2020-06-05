import logging
import requests
from p2myconfig.config import HEADERS
import traceback
import json


def sendPost(url, iname="", info=None):
    info = {} if not info else info
    '''
    :param iname: 接口名称 str
    :param info: 参数 dict
    :param flag: bool  是否检查返回状态
    :return: 接口请求结果
    '''
    logging.debug(iname + "接口核算请求地址：" + url)
    logging.debug(iname + "接口请求参数：" + str(info))
    try:
        rev = requests.post(url=url, data=json.dumps(info), headers=HEADERS, timeout=30)
    except Exception as e:
        logging.error(iname + "接口调用失败")
        traceback.print_exc()
        raise e
    return rev


def sendGet(url, iname="", info=None):
    info = {} if not info else info
    '''
    :param iname: 接口名称 str
    :param info: 参数 dict
    :param flag: bool  是否检查返回状态
    :return: 接口请求结果
    '''
    logging.debug(iname + "接口核算请求地址：" + url)
    logging.debug(iname + "接口请求参数：" + str(info))
    try:
        rev = requests.get(url=url, data=json.dumps(info), timeout=30)
    except Exception as e:
        logging.error(iname + "接口调用失败")
        traceback.print_exc()
        raise e
    return rev

if __name__ == '__main__':
    result = sendPost(url="http://www.baidu.com", iname="my", info="{}")
    print(result)


