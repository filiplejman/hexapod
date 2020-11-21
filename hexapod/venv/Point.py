class Operation:
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_coordinates(self):
        return self.x, self.y, self.z

    def operation(self, p, op=Operation.ADD):
        func = [lambda x, y: x+y, lambda x, y: x-y, lambda x, y: x*y]
        self.x = func[op](self.x, p.x)
        self.y = func[op](self.y, p.y)
        self.z = func[op](self.z, p.z)

    def __str__(self):
        return "x: {} | y: {} | z: {}".format(self.x, self.y, self.z)

    __repr__ = __str__


if __name__ == "__main__":
    p1 = Point(1, 2, 3)
    p2 = Point(4, 5, 8)
    print(Operation.ADD)
    p1.operation(p2, Operation.MULTIPLY)
    print(p1)
