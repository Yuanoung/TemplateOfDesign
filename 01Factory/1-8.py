class Operation(object):
    @staticmethod
    def getResult(numberA, op, numberB):
        if op == "+":
            return numberA + numberB
        elif op == "-":
            return numberA - numberB
        elif op == "*":
            return numberA * numberB
        else:
            return numberA / numberB