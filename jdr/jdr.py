import random


class AddPool:
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __repr__(self):
        return repr(self.l) + " + " + repr(self.r)

    def throw(self):
        return self.l.throw() + self.r.throw()

    def show(self):
        return str(self.l.show()) + ", " + str(self.r.throw())


class MultPool:
    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.v = []

    def __repr__(self):
        return repr(self.l) + repr(self.r)

    def throw(self):
        result = 0
        i = 0
        self.v = []
        while i < self.l:
            tmp = self.r.throw()
            result += tmp
            self.v.append(tmp)
            i += 1
        return result

    def show(self):
        result = ""
        for i in self.v:
            result += str(i) + ", "
        return result[:len(result) - 2]


class Pool:
    min = 1
    max = 1

    def __init__(self, op, v=None):
        self.op = op
        # print("> ", op)
        self.result = 0
        self.str = v if v else repr(op)

    def __add__(self, thing):
        if isinstance(thing, int):
            thing = FrozenDice(thing)
        return Pool(AddPool(self, thing))

    def __mul__(self, c: int):
        if not isinstance(c, int):
            raise TypeError("the multiplicator is obviously a int not a %s" % type(c))
        return Pool(MultPool(c, self))

    def __radd__(self, thing):
        if isinstance(thing, int):
            thing = FrozenDice(thing)
        return Pool(AddPool(thing, self))

    def __rmul__(self, c: int):
        if not isinstance(c, int):
            raise TypeError("the multiplicator is obviously a int not a %s" % type(c))
        return Pool(MultPool(c, self))

    def throw(self):
        if self.op:
            self.result = self.op.throw()
        else:
            self.result = random.randint(self.min, self.max)
        return self.result

    def show(self):
        if self.op:
            return str(self.op.show())
        else:
            return str(self.result)

    def roll(self, v=None):
        f = False
        if v is None:
            f = True
            v = []
        if self.op is None:
            v.append(self.max)
        else:
            if isinstance(self.op, AddPool):
                self.op.l.roll(v)
                self.op.r.roll(v)
            else:
                i = 0
                while i < self.op.l:
                    self.op.r.roll(v)
                    i += 1
        if f:
            t = ()
            ta = []
            for _ in v:
                t = t + (1,)
            while True:
                ta.append(t)
                u = ()
                for w in t:
                    u = u + (w,)
                t = u
                i = len(v) - 1
                while i >= 0:
                    t = change_tuple(t, i, t[i] + 1)
                    if t[i] > v[i]:
                        t = change_tuple(t, i, 1)
                        j = i + 1
                        while j < len(v):
                            t = change_tuple(t, j, 1)
                            j += 1
                    else:
                        break
                    i -= 1
                if i == -1:
                    break
            return my_yield(ta)

    def __repr__(self):
        return self.str


class AbstractResult(Pool):
    def __init__(self, v):
        super().__init__(None, v)

    @staticmethod
    def seed(s):
        random.seed(s)


class FrozenDice(AbstractResult):
    def __init__(self, v):
        super().__init__(str(v))
        self.result = v

    def __repr__(self):
        return str(self.result)

    def throw(self):
        return self.result


class D4(AbstractResult):
    def __init__(self):
        super().__init__("D4")
        self.max = 4


class D6(AbstractResult):
    def __init__(self):
        super().__init__("D6")
        self.max = 6


class D8(AbstractResult):
    def __init__(self):
        super().__init__("D8")
        self.max = 8


class D10(AbstractResult):
    def __init__(self):
        super().__init__("D10")
        self.max = 10


class D12(AbstractResult):
    def __init__(self):
        super().__init__("D12")
        self.max = 12


class D20(AbstractResult):
    def __init__(self):
        super().__init__("D20")
        self.max = 20


d4 = D4()
d6 = D6()
d8 = D8()
d10 = D10()
d12 = D12()
d20 = D20()


def change_tuple(t, i, v):
    u = ()
    j = 0
    while j < len(t):
        u = u + ((t[j],) if j != i else (v,))
        j += 1
    return u


def my_yield(ta):
    for i in ta:
        yield i
