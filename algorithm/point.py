class Point(object):
    def __init__(self, points: list, size=0) -> None:
        self.points = points
        if size <= 0:
            return
            
        while len(self.points) < size:
            self.points.append(self.points[0])

        while len(self.points) > size:
            self.points.pop()

    def copy(self):
        return Point([x for x in self.points])

    def sum(self):
        return sum(self.points)
    
    def __lt__(self, other):
        for x, y in zip(self.points, other.points):
            if x < y:
                return True
            elif x > y:
                return False
        return False
    
    def __gt__(self, other):
        for x, y in zip(self.points, other.points):
            if x > y:
                return True
            elif x < y:
                return False
        return False

    def __eq__(self, o) -> bool:
        for x, y in zip(self.points, o.points):
            if x != y:
                return False
        return True
    
    def __ge__(self, o):
        return (self > o or self == o)
    
    def __le__(self, o):
        return (self < o or self == o)

    def __add__(self, other):
        return Point([x + y for x, y in zip(self.points, other.points)])

    def __mul__(self, x):
        return Point([y * x for y in self.points])

    def __str__(self) -> str:
        return str(self.points)


# a = Point([1, 2, 3])
# b = Point([1, 2, 3])

# print(a < b)
# print(a == b)
# print(a > b)
# print(a <= b)
# print(a >= b)