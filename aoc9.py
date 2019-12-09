import itertools as it
import operator as op

class DataPointer:

    def __init__(self, data):
        self.__data = data
        self.__idx = 0

    def __iter__(self):
        return self

    def jump(self, idx):
        self.__idx = idx

    def __next__(self):
        try:
            return self.__data[self.__idx]
        except IndexError:
            raise StopIteration
        finally:
            self.__idx += 1


class Computer:

    def __init__(self, data):
        self.__config(data)
        self.__halted = False
        self.__relativeBase = 0

    def __config(self, data):
        self.__data = data
        self.__data.extend(0 for _ in range(1000000))
        self.__data_ptr = DataPointer(self.__data)

    def run(self, inp=None):
        self.__input = inp

        while((i := self.__shift()) != 99):
            opcode, mode = self.__parseInstruction(str(i))
            if (opcode == 1):
                self.__calc(op.add, mode)
            elif (opcode == 2):
                self.__calc(op.mul, mode)
            elif (opcode == 3):
                self.__write(mode)
            elif (opcode == 4):
                self.__lastRead = self.__read(mode)
            elif (opcode == 5):
                self.__jumpIf(op.ne, mode)
            elif (opcode == 6):
                self.__jumpIf(op.eq, mode)
            elif (opcode == 7):
                self.__storeOneIf(op.lt, mode)
            elif (opcode == 8):
                self.__storeOneIf(op.eq, mode)
            elif (opcode == 9):
                self.__adjustRelativeBase(mode)

        self.__halted = True
        return self.__lastRead

    def __shift(self):
        return next(self.__data_ptr)

    def __parseInstruction(self, inst):
        opcode = int(inst[-2:])

        if (opcode == 3):
            p = int(format(inst[:-2], '0>1'))
            if (p != 0):
                return opcode, p
            return opcode, None

        elif (opcode == 4):
            p = int(format(inst[:-2], '0>1'))
            return opcode, p

        elif (opcode == 9):
            p = int(format(inst[:-2], '0>1'))
            return opcode, p

        p1, p2, p3 = [int(s) for s in format(inst[:-2], '0>3')[::-1]]
        return opcode, (p1, p2, p3)

    def __calc(self, operation, mode):
        pos1 = self.__getData(mode[0])
        pos2 = self.__getData(mode[1])
        out = operation(pos1, pos2)
        if mode[2] == 2:
            self.__data[self.__shift() + self.__relativeBase] = out
        else:
            self.__data[self.__shift()] = out

    def __write(self, mode):
        if (mode == 2):
            self.__data[self.__shift() + self.__relativeBase] = self.__input
        else:
            self.__data[self.__shift()] = self.__input

    def __read(self, mode):
        return self.__getData(mode)

    def __jumpIf(self, operation, mode):
        if (operation(self.__getData(mode[0]), 0)):
            self.__data_ptr.jump(self.__getData(mode[1]))
        else:
            self.__shift()

    def __storeOneIf(self, operation, mode):
        val = 0
        if (operation(self.__getData(mode[0]), self.__getData(mode[1]))):
            val = 1

        if mode[2] == 2:
            self.__data[self.__shift() + self.__relativeBase] = val
        else:
            self.__data[self.__shift()] = val

    def __adjustRelativeBase(self, mode):
        self.__relativeBase += self.__getData(mode)

    def __getData(self, mode):
        if (mode == 1):
            return self.__shift()

        if (mode == 2):
            return self.__data[self.__shift() + self.__relativeBase]

        return self.__data[self.__shift()]

    def getResult(self):
        return self.__data[0]

    def wasHalted(self):
        return self.__halted

data = [int(i) for i in open('input.txt', 'r').readline().split(',')]

print("1:", Computer(data.copy()).run(1))
print("2:", Computer(data.copy()).run(2))