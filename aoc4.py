from collections import Counter
from itertools import tee


bottom, top = (int(i) for i in open('input.txt', 'r').readline().split('-'))
numbers = (str(n) for n in range(bottom, top + 1))


def partOneCriteria(num):
	isPair = False
	for a, b in pairwise(num):
		if a > b:
			return False

		if a == b:
			isPair = True

	return isPair


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def partTwoCriteria(num):
	return 2 in Counter(num).values()


viableNums = [num for num in numbers if partOneCriteria(num)]


partOneCriteriaAmount = len(viableNums)
print("1:", partOneCriteriaAmount)

partTwoCriteriaAmount = sum(partTwoCriteria(num) for num in viableNums)
print("2:", partTwoCriteriaAmount)

