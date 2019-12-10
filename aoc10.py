import itertools as it
import math
from functools import cmp_to_key as ctk 


def collect_asteroids_coordinates(data):
    asteroids = []

    for idy, line in enumerate(data):
        for idx, point in enumerate(line):
            if point == '#':
                asteroids.append((idx, idy))
    return asteroids


def is_visible(p1, p2):
    if (p1 == p2):
        return False

    vec = (p2[0] - p1[0], p2[1] - p1[1])

    if (abs(vec[0]) < 2 and abs(vec[1]) < 2):
        return True

    step = math.gcd(abs(vec[0]), abs(vec[1]))
    if step == 1:
        return True

    step_vector = (vec[0] // step, vec[1] // step)

    intersecting_point = p1
    while((intersecting_point := tuple(map(sum, zip(intersecting_point, step_vector)))) != p2):
        if intersecting_point in asteroids:
            return False
    return True


def find_best_location(asteroids):
    location = tuple()
    num_of_visible = int()
    for point in asteroids:
        num = sum(is_visible(point, p2) for p2 in asteroids)
        if num > num_of_visible:
            num_of_visible = num
            location = point
    return location, num_of_visible


data = [i for i in open('input.txt', 'r').read().splitlines()]
asteroids = collect_asteroids_coordinates(data)

laser_pos, num_of_visible = find_best_location(asteroids)
print("1:", num_of_visible)


cmp = lambda a, b: (a > b) - (a < b)
sign = lambda i: (i > 0) - (i < 0)

def compare_angle(p1, p2):
    dp1 = p1[0] < 0
    dp2 = p2[0] < 0

    if (dp1 != dp2):
        return cmp(dp1, dp2)

    if (p1[0] == 0 and p2[0] == 0):
        return cmp(sign(p1[1]), sign(p2[1]))

    return sign(p1[0] * p2[1] - p1[1] * p2[0])


viable_asteroids = [p for p in asteroids if is_visible(laser_pos, p)]
relative_asteroids_pos = [(p[0] - laser_pos[0], p[1] - laser_pos[1]) for p in viable_asteroids]
asteroids_sorted = sorted(relative_asteroids_pos, key=ctk(compare_angle), reverse=True)

point_at_twelve = asteroids_sorted.index(next(p for p in asteroids_sorted if p[0] == 0 and p[1] < 0))
asteroids_sorted = asteroids_sorted[point_at_twelve:] + asteroids_sorted[:point_at_twelve - 1] # temporary workaround XD

print("2:", (asteroids_sorted[199][0] + laser_pos[0]) * 100 + asteroids_sorted[199][1] + laser_pos[1])