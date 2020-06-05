import enum


class TractionType(enum.Enum):
    putout = ("putout", "1001")
    flexibleputout = ("flexiblePutout", "1001")
    endofday = ("ENDOFDAY", "9090")
    prepayback = ("prepayback", "2001")
    normalpayback = ("normalpayback", "2002")

    # 相等判断
    def equals(self, ops2):
        if isinstance(ops2, TractionType) and self.name == ops2.name and self.value == ops2.value:
            return True
        return False

    # 打印格式
    def __str__(self):
        return '%s' % (self.name)

    def __repr__(self):
        return '%s' % (self._name_)

    # def __new__(cls, value):
    #     if type(value) is cls:
    #         return value
    #     print([name[0] for name in cls._value2member_map_.keys()])
    #     try:
    #         if value in [name[0] for name in cls._value2member_map_.keys()]:
    #             return cls._value2member_map_[value]
    #     except TypeError:
    #         for member in cls._member_map_.values():
    #             if member._value_ == value:
    #                 return member
    #     return cls._missing_(value)


if __name__ == '__main__':
    # print(TractionType.__new__(TractionType,"putout"))
    print(TractionType.normalpayback)
