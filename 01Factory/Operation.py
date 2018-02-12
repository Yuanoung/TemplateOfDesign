import abc


class Operation(abc.ABC):
    def __init__(self, numberA, numberB):
        self._numberA = numberA
        self._numberB = numberB

    @abc.abstractmethod
    def getResult(self):
        raise NotImplementedError


class OperationAdd(Operation):
    def __init__(self, numberA, numberB):
        super(OperationAdd, self).__init__(numberA, numberB)

    def getResult(self):
        return self._numberA + self._numberB


class OperationSub(Operation):
    def __init__(self, numberA, numberB):
        super(OperationSub, self).__init__(numberA, numberB)

    def getResult(self):
        return self._numberA - self._numberB


class OperationMul(Operation):
    def __init__(self, numberA, numberB):
        super(OperationMul, self).__init__(numberA, numberB)

    def getResult(self):
        return self._numberB * self._numberA


class OperationDiv(Operation):
    def __init__(self, numberA, numberB):
        super(OperationDiv, self).__init__(numberA, numberB)

    def getResult(self):
        try:
            return self._numberA / self._numberB
        except ZeroDivisionError:
            return "除数不能为0"


class OperationFactory(object):
    _select = {
        "+": OperationAdd,
        "-": OperationSub,
        "*": OperationMul,
        "/": OperationDiv
    }

    @staticmethod
    def createOperation(op):
        return OperationFactory._select.get(op)


def isValidate(op):
    if op not in "-+/*":
        print("操作符无效， 必须是'- * / +'中的任何一个")
        exit(0)


if __name__ == "__main__":
    numberA = int(input("请输入数字:\n>>> "))
    op = input("请输入运算符:\n>>> ")
    isValidate(op)
    numberB = int(input("请输入另一个数字:\n>>> "))

    opCls = OperationFactory.createOperation(op)
    operation = opCls(numberA, numberB)
    print(operation.getResult())

