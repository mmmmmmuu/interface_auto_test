import logging, json
from copy import copy
from p5common.tempVariable import TempVariable


def saveParam(func):
    def wrapper(*args, **kwargs):
        {"record": recordparam, "check": checkparam}["model"](args[0], args[1])
        rev = func(args[0], args[1], **kwargs)
        return rev
    return wrapper

def recordparam(method):
    pass

def checkparam(method):
    pass


def iter_replace(info, args):
    for key, value in args.items():
        if key in info.keys():
            if isinstance(value, dict) and info[key]:
                iter_replace(info[key], value)
            else:
                info[key] = copy(value)

# def paramNotNone(func):
#     '''参数非空check装饰器1111111'''
#     def wrapper(*args):
#         for value in args:
#             if value is None:
#                 logging.error(str(value) + "为空，请检查！")
#         return func(args)
#     return wrapper

# def resultCheck(func):
#     '''返回结果校验'''
#     def warpper(*args,**kwargs):
#         rev = func(*args,**kwargs)
#         if "flag" in kwargs.keys() and kwargs["flag"]:
#             if rev.status_code != 200:
#                 logging.error(kwargs["tranName"] + "接口返回状态为" + str(rev.status_code) +",接口不为200!")
#                 raise RuntimeError(kwargs["tranName"] + "接口返回状态为" + str(rev.status_code) +",接口不为200!")
#             result = json.loads(rev.content)
#             if not result["result"]:
#                 desc=""
#                 if "returnMessage" in result.keys() and result["returnMessage"] is not None and result["returnMessage"]:
#                     desc = "返回信息为：" + str(result["returnMessage"])
#                 logging.error(kwargs["tranName"] + "返回结果为false，请检查！" + desc)
#                 raise RuntimeError(kwargs["tranName"] + "返回结果为false，请检查！" + desc)
#         return rev
#     return warpper

#
# def recordrequest(func):
#     def wrapper(*args, **kwargs):
#         dbopr = Dboperator(test_db)
#
#     return wrapper()




