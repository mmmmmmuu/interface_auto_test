
import importlib
from p0constants.batch_constants import *
from p5common.tempVariable import TempVariable

class common_utils:

    _cage = {}
    _plugins = []

    def __init__(self, instance):
        self._ref = {BATCH_BATCH: "influence_batch", BATCH_GROUP: "influence_group", BATCH_INTERFACE: "influence_interface"}
        self._plugins = TempVariable.cage[instance._batch_no]["plugins"]
        for plugin in self._plugins:
            util = importlib.import_module("p7plugins." + plugin["execute_class"])
            self._cage[plugin["execute_class"]] = getattr(util, plugin["execute_class"])(instance)


    # 执行插件方法
    def runPlugins(self, type, method, check_type=1, **kwargs):   # 1： 无返回  2：任意返回false返回
        for plugin in self._plugins:
            if plugin[self._ref[type]]:
                m = getattr(self._cage[plugin["execute_class"]], method)
                result = m(**kwargs)
                if check_type == 2 and not result[0]:
                    return result
        if check_type == 2:
            return True, ""


    def runActions(self):
        pass


if __name__ == '__main__':
    re = importlib.import_module("p7plugins.request_utils")
    cl = getattr(re, "requestUtils")
    print(cl)
