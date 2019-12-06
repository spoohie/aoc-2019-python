from functools import reduce

def calculateFuel(fuel):
	additionalFuel = int(fuel/3)-2
	if (additionalFuel < 0):
		return 0

	return additionalFuel + calculateFuel(additionalFuel)

data = [int(i) for i in open('input.txt', 'r')]

print("1:", sum(fuel // 3 - 2 for fuel in data))
print("2:", sum(calculateFuel(fuel) for fuel in data))