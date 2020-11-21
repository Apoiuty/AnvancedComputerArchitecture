print(None in set())


class A:
    pass


a1 = A()
a2 = A()
s = {a1}
print(a1 in s)
