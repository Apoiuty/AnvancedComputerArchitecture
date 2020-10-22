"""
内存类和函数，内存采用页式内存管理，并实现了一些内存相关函数
"""
import numpy as np

# 页表，只存储物理虚拟地址和物理地址之间的映射
Available_Addr = 0  # 可用页


def addr_mode(addr):
    """
    寻址方式确定，并返回绝对地址（目前只实现直接寻址）
    # TODO
    :param addr: 地址字符串
    :return: 绝地址
    """
    if addr.startswith('#'):
        return int(addr[1:])


def check_boundary(addr, n):
    """
    检查addr是否在0-2^n-1范围内
    :param addr:
    :param n:
    :return: bool
    """
    return 0 <= addr < 2 ** n


class Word:
    """
    字类型
    """

    def __init__(self):
        """
        创建字，字长为32位
        """
        self.__data = None

    def __getitem__(self, item):
        """
        获取内存中内存单元内容
        :return: 单元内容
        """
        return self.__data[0]

    def __setitem__(self, key, value):
        """
        设置内存页中的数据
        :param value: 值
        :return:
        """
        if isinstance(value, int):
            self.__data = np.array([value], dtype=np.int32)
        elif isinstance(value, float):
            self.__data = np.array([value], dtype=np.float32)


class Memory:
    """
    内存类
    """

    def __init__(self):
        """
        创建内存对象,用列表来存储已经分配到内存中的字
        """
        self.__memory = {}

    def __getitem__(self, addr):
        """
        返回地址addr中的内存单元内容
        :param addr: 地址
        :return: 数据
        """
        if addr in self.__memory:
            return self.__memory[addr][0]
        else:
            # 访问的地址未在内存中分配
            print("Invalid address.")

    def __setitem__(self, addr, value):
        """
        写内存
        :param addr: 地址
        :param value: 值
        :return:
        """
        global Available_Addr
        if addr in self.__memory:
            self.__memory[addr][0] = value
        else:
            # 分配页
            if Available_Addr < 2 ** 32:
                self.__memory[addr] = Word()
                Available_Addr += 1
                self.__memory[addr][0] = value
            else:
                print("Not enough memory.")
                raise Exception


# 创建内存对象
memory = Memory()
