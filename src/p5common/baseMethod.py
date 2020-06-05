
from p5common.common import common_utils

class baseMethod:

    def _skipcheck(self):
        return True, ""

    def _exitcheck(self):
        return True, ""

    # 替换变量
    def _dealParams(self):
        pass

    # 保存变量
    def _saveParams(self):
        pass

    # 执行前做 如打印执行日志
    def _dobefore(self):
        pass

    # 执行自定义动作
    def _preaction(self):
        pass

    # 执行
    def _run(self):
        pass

    # 返回结果检查
    def _response_check(self):
        return True, ""

    # 处理返回
    def _dealResponse(self):
        pass

    # 讲执行结果保存到内存供后续引用
    def _saveResponse(self):
        pass

    # 执行自定义后置动作
    def _ateraction(self):
        pass

    # 执行后操作 如打印日志
    def _doafter(self):
        pass

if __name__ == '__main__':
    b = baseMethod()
    print(b.__dict__)


