UP = 0, 1
DOWN = 0, -1
LEFT = -1, 0
RIGHT = 1, 0

def calculateDist(dist):
    return abs(dist[0]) + abs(dist[1])

class Wire:

    def __init__(self, data):
        self.__data = data
        self.__currentPos = (0,0)
        self.__path = []

        self.__calculatePath()

    def __calculatePath(self):
        for command in self.__data:
            course, num = self.__parse(command)
            self.__move(course, num)

    def __parse(self, command):
        return command[0], int(command[1:])

    def __move(self, course, num):
        if(course == 'U'):
            [self.__step(UP) for _ in range(num)]

        elif(course == 'D'):
            [self.__step(DOWN) for _ in range(num)]         

        elif(course == 'L'):
            [self.__step(LEFT) for _ in range(num)]

        elif(course == 'R'):
            [self.__step(RIGHT) for _ in range(num)]

    def __step(self, direction):
        self.__currentPos = tuple(map(sum, zip(self.__currentPos, direction)))
        self.__path.append(self.__currentPos)

    def getPath(self):
        return self.__path

    def getWireDistance(self, intersection):
        return self.__path.index(intersection) + 1


data = [[i for i in wire.rstrip().split(',')] for wire in open('input.txt', 'r')]

wire = [Wire(d) for d in data]

common = set(wire[0].getPath()) & set(wire[1].getPath())

closest = min(calculateDist(dist) for dist in common)
print("1:", closest)

closestByWireLength = min(wire[0].getWireDistance(dist) + wire[1].getWireDistance(dist) for dist in common)
print("2:", closestByWireLength)