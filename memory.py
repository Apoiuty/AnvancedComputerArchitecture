"""
内存类和函数，内存采用页式内存管理，并实现了一些内存相关函数
"""
import numpy as np

# 页表，只存储物理虚拟地址和物理地址之间的映射
Available_Addr = 0  # 可用页


class Imm:
    """
    立即数对象
    """

    def __init__(self):
        pass

    def __getitem__(self, item):
        if isinstance(item, int):
            return np.int32(item)
        elif isinstance(item, float):
            return np.float32(item)


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
        if isinstance(value, int) or isinstance(value, np.int32):
            self.__data = np.array([value], dtype=np.int32)
        elif isinstance(value, float) or isinstance(value, np.float32):
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


