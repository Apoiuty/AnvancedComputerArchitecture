"""
内存类和函数，内存采用页式内存管理，并实现了一些内存相关函数
"""
import numpy as np

Page_Table = {}
# 页表，只存储物理虚拟地址和物理地址之间的映射
Available_Page = list(range(0, 2 ** 20))  # 可用页


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


class Page:
    """
    内存页类型
    """
    __page_size = 12  # 页大小

    def __init__(self):
        """
        创建内存页，每个页大小为4Kb
        """
        self.__page = np.random.randint(0, 255, (2 ** self.__page_size, 1), dtype=np.uint8)

    def __getitem__(self, addr):
        """
        获取内存中内存单元内容
        :param addr: 页中偏移地址
        :return: 单元内容
        """
        if check_boundary(addr, self.__page_size):
            return self.__page[addr][0]
        else:
            print("Out of index.\n")
            raise IndexError

    def __setitem__(self, addr, value):
        """
        设置内存页中的数据
        :param addr: 地址
        :param value: 值
        :return:
        """
        if check_boundary(addr, self.__page_size):
            self.__page[addr][0] = value
        else:
            print("Out of index.\n")
            raise IndexError


class Memory:
    """
    内存类
    """

    def __init__(self):
        """
        创建内存对象,用字典来存储已经分配到内存中的页，字典的键为页号，值为page对象
        """
        self.__memory = {}

    def __getitem__(self, addr):
        """
        返回地址addr中的内存单元内容
        :param addr: 地址
        :return: 数据
        """
        page_size = 2 ** 12
        page_num = addr // page_size
        if page_num in Page_Table:
            addr = addr % page_size
            return self.__memory[Page_Table[page_num]][addr]
        else:
            # 访问的地址不在页表中，无法翻译
            print("Invalid address.\n")

    def __setitem__(self, addr, value):
        """
        写内存
        :param addr: 地址
        :param value: 值
        :return:
        """
        page_size = 2 ** 12
        page_num = addr // page_size
        addr = addr % page_size
        if page_num in Page_Table:
            self.__memory[Page_Table[page_num]][addr] = value
        else:
            # 分配页
            if Available_Page:
                physics_page = Available_Page[0]
                Available_Page.pop(0)
                Page_Table[page_num] = physics_page
                self.__memory[physics_page] = Page()
                self.__memory[physics_page][addr] = value
            else:
                # 如果内存不足则不继续分配物理页，先不考虑辅存中页交换
                print("Not enough memory.\n")
                raise Exception


# 创建内存对象
memory = Memory()
