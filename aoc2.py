import itertools as it

class Computer:

    def __init__(self, data, i1, i2):
        self.__config(data)
        self.__setInput(i1, i2)
        self.__run()

    def __config(self, data):
        self.__data = data
        self.__data_iterator = iter(self.__data)

    def __setInput(self, i1, i2):
        self.__data[1] = i1
        self.__data[2] = i2

    def __run(self):
        while((i := self.__shift()) != 99):
            if(i == 1):
                self.__add()
            elif(i == 2):
                self.__multiply()

    def __shift(self):
        return next(self.__data_iterator)
        
    def __add(self):
        pos1 = self.__data[self.__shift()]
        pos2 = self.__data[self.__shift()]
        self.__data[self.__shift()] = pos1 + pos2

    def __multiply(self):
        pos1 = self.__data[self.__shift()]
        pos2 = self.__data[self.__shift()]
        self.__data[self.__shift()] = pos1 * pos2

    def getResult(self):
        return self.__data[0]


data = [int(i) for i in open('input.txt', 'r').readline().split(',')]

computer = Computer(data.copy(), 12, 2)
print("1:", computer.getResult())

for i1, i2 in it.product(range(0, 100), range(0, 100)):
    computer = Computer(data.copy(), i1, i2)
    if computer.getResult() == 19690720:
        print("2:", 100 * i1 + i2)
        break