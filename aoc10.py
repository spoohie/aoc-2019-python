import math
import itertools as it
from copy import deepcopy

def collect_asteroids_coordinates(data):
    asteroids = []

    for idy, line in enumerate(data):
        for idx, point in enumerate(line):
            if point == '#':
                asteroids.append((idx, idy))
    return asteroids

def isVisible(p1, p2):
    if (p1 == p2):
        return False

    vec = (p2[0] - p1[0], p2[1] - p1[1])

    if (abs(vec[0]) < 2 and abs(vec[1]) < 2):
        return True

    step = math.gcd(abs(vec[0]), abs(vec[1]))
    if step == 1:
        return True

    step_vector = (vec[0] // step, vec[1] // step)

    intersecting_point = deepcopy(p1)
    while((intersecting_point := tuple(map(sum, zip(intersecting_point, step_vector)))) != p2):
        if intersecting_point in asteroids:
            return False
    return True

data = [i for i in open('input.txt', 'r').read().splitlines()]
asteroids = collect_asteroids_coordinates(data)

num = max(sum(isVisible(point, p2) for p2 in asteroids) for point in asteroids)
print("1:", num)

