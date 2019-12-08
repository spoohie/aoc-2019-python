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

    def __init__(self, data, i):
        self.__config(data)
        self.__input = i
        self.__run()

    def __config(self, data):
        self.__data = data
        self.__data_ptr = DataPointer(self.__data)

    def __run(self):
        while((i := self.__shift()) != 99):
            opcode, mode = self.__parseInstruction(str(i))
            if (opcode == 1):
                self.__calc(op.add, mode)
            elif (opcode == 2):
                self.__calc(op.mul, mode)
            elif (opcode == 3):
                self.__write()
            elif (opcode == 4):
                self.__read(mode)
            elif (opcode == 5):
                self.__jumpIf(op.ne, mode)
            elif (opcode == 6):
                self.__jumpIf(op.eq, mode)
            elif (opcode == 7):
                self.__storeOneIf(op.lt, mode)
            elif (opcode == 8):
                self.__storeOneIf(op.eq, mode)

    def __shift(self):
        return next(self.__data_ptr)

    def __parseInstruction(self, inst):
        opcode = int(inst[-2:])

        if (opcode == 3):
            return opcode, None

        elif (opcode == 4):
            p = int(format(inst[:-2], '0>1'))
            return opcode, p
        p1, p2 = [int(s) for s in format(inst[:-2], '0>2')[::-1]]
        return opcode, (p1, p2)

    def __calc(self, operation, mode):
        pos1 = self.__getData(mode[0])
        pos2 = self.__getData(mode[1])
        self.__data[self.__shift()] = operation(pos1, pos2)

    def __write(self):
        self.__data[self.__shift()] = self.__input

    def __read(self, mode):
        self.__diagnosticCode = self.__getData(mode)

    def __jumpIf(self, operation, mode):
        if (operation(self.__getData(mode[0]), 0)):
            self.__data_ptr.jump(self.__getData(mode[1]))
        else:
            self.__shift()

    def __storeOneIf(self, operation, mode):
        val = 0
        if (operation(self.__getData(mode[0]), self.__getData(mode[1]))):
            val = 1
        self.__data[self.__shift()] = val

    def __getData(self, mode):
        if (mode == 1):
            return self.__shift()

        return self.__data[self.__shift()]

    def getResult(self):
        return self.__data[0]

    def getDiagnosticCode(self):
        return self.__diagnosticCode


data = [int(i) for i in open('input.txt', 'r').readline().split(',')]

computer = Computer(data.copy(), 1)
print("1:", computer.getDiagnosticCode())

computer = Computer(data.copy(), 5)
print("2:", computer.getDiagnosticCode())