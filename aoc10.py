import itertools as it
import math
from collections import namedtuple
from functools import cmp_to_key as ctk

Point = namedtuple('Point', 'x y')


def collect_asteroids_coordinates(data):
    asteroids = []

    for idy, line in enumerate(data):
        for idx, point in enumerate(line):
            if point == '#':
                asteroids.append(Point(idx, idy))
    return asteroids


def find_best_location(asteroids):
    num_of_visible = int()
    for point in asteroids:
        num = sum(is_visible(point, p2) for p2 in asteroids)
        if num > num_of_visible:
            num_of_visible = num
            location = point
    return location, num_of_visible


def is_visible(p1, p2):
    if (p1 == p2):
        return False

    vec = Point(p2.x - p1.x, p2.y - p1.y)
    if (abs(vec.x) < 2 and abs(vec.y) < 2):
        return True

    step = math.gcd(abs(vec.x), abs(vec.y))
    if step == 1:
        return True

    step_vector = Point(vec.x // step, vec.y // step)
    intersecting_point = p1
    while((intersecting_point := tuple(map(sum, zip(intersecting_point, step_vector)))) != p2):
        intersecting_point = Point(intersecting_point[0], intersecting_point[1])
        if intersecting_point in asteroids:
            return False
    return True


data = [i for i in open('input.txt', 'r').read().splitlines()]
asteroids = collect_asteroids_coordinates(data)

laser_pos, num_of_visible = find_best_location(asteroids)
print("1:", num_of_visible)


def compare_angle(p1, p2):
    dp1 = p1.x < 0
    dp2 = p2.x < 0
    if (dp1 != dp2):
        return cmp(dp1, dp2)
    if (p1.x == 0 and p2.x == 0):
        return cmp(sign(p1.y), sign(p2.y))
    return sign(p1.x * p2.y - p1.y * p2.x)


cmp = lambda a, b: (a > b) - (a < b)
sign = lambda i: (i > 0) - (i < 0)


viable_asteroids = [p for p in asteroids if is_visible(laser_pos, p)]
relative_asteroids_pos = [Point(p.x - laser_pos.x, p.y - laser_pos.y) for p in viable_asteroids]
asteroids_sorted = sorted(relative_asteroids_pos, key=ctk(compare_angle), reverse=True)

point_at_twelve = asteroids_sorted.index(next(p for p in asteroids_sorted if p.x == 0 and p.y < 0))
asteroids_sorted = asteroids_sorted[point_at_twelve:] + asteroids_sorted[:point_at_twelve - 1] # temporary workaround XD

print("2:", (asteroids_sorted[199].x + laser_pos.x) * 100 + asteroids_sorted[199].y + laser_pos.y)