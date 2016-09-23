import random


class AbstractResult:
    min = 1
    max = 1

    def __init__(self):
        self.result = 0

    def __add__(self, thing):
        if isinstance(thing, int):
            thing = FrozenDice(thing)
        return Pool([self] + [thing])

    def __mul__(self, c: int):
        if not isinstance(c, int):
            raise TypeError("the multiplicator is obviously a int not a %s" % type(c))
        return Pool([self] * c)

    def __repr__(self):
        return type(self).__name__

    def throw(self):
        self.result = random.randint(type(self).min, type(self).max)
        return self.result

    def seed(s):
        random.seed(s)


class FrozenDice(AbstractResult):
    def __init__(self, v):
        super().__init__()
        self.result = v

    def __repr__(self):
        return str(self.result)

    def throw(self):
        return self.result


class D4(AbstractResult):
    max = 4
