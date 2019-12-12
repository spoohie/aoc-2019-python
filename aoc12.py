import itertools as it
from collections import namedtuple


Coords = namedtuple('Coordinates', 'x y z')


class Moon:
    def __init__(self, pos):
        self.__pos = pos
        self.__vel = Coords(0, 0, 0)

    def get_pos(self):
        return (self.__pos.x, self.__pos.y, self.__pos.z)

    def update_vel(self, x, y, z):
        self.__vel = Coords(self.__vel.x + x, self.__vel.y + y, self.__vel.z + z)

    def update_pos(self):
        self.__pos = Coords(self.__pos.x + self.__vel.x, self.__pos.y + self.__vel.y, self.__pos.z + self.__vel.z)

    def get_energy(self):
        return (abs(self.__vel.x) + abs(self.__vel.y) + abs(self.__vel.z)) * (abs(self.__pos.x) + abs(self.__pos.y) + abs(self.__pos.z))


def calculate_gravity_relation(moon1, moon2):
    vel_correction = [0, 0, 0]
    for i, (c1, c2) in enumerate(zip(moon1.get_pos(), moon2.get_pos())):
        vel_correction[i] = cmp(c2, c1)
    moon1.update_vel(vel_correction[0], vel_correction[1], vel_correction[2])
    moon2.update_vel(-vel_correction[0], -vel_correction[1], -vel_correction[2])

cmp = lambda a, b: (a > b) - (a < b)


data = [[int(i.split('=')[1]) for i in moon[1:-1].split(',')] for moon in open('input.txt', 'r').read().splitlines()]

moons = [Moon(Coords(m[0], m[1], m[2])) for m in data]

for _ in range(1000):
    [calculate_gravity_relation(m1, m2) for m1, m2 in it.combinations(moons, 2)]
    [moon.update_pos() for moon in moons]

total_energy = sum(moon.get_energy() for moon in moons)
print("1:", total_energy)