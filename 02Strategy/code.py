import abc


class CashSuper(abc.ABC):
    @abc.abstractclassmethod
    def acceptCash(self, money):
        """收取现金，参数为原价，返回为当前价"""
        raise NotImplementedError


class CashNormal(CashSuper):
    """正常收款"""

    def acceptCash(self, money):
        return money


class CashRebate(CashSuper):
    """打折类"""

    def __init__(self, rebate=1.0):
        self._rebate = rebate

    def acceptCash(self, money):
        return money * self._rebate


class CashReturn(CashSuper):
    """满几减几

    ex:
        满３００减１００，则condition=300, free=100
    """

    def __init__(self, condition, free):
        self._condition = condition
        self._free = free

    def acceptCash(self, money):
        if money >= self._condition:
            return money - (money // self._condition) * self._free
        else:
            return money


class CashFactory(object):
    """现金收取工厂"""

    @staticmethod
    def createCashAccept(alg):
        cs = None
        if alg == "正常收费":
            cs = CashNormal()
        elif alg == "满３００减５０":
            cs = CashReturn(300, 50)
        elif alg == "8折":
            cs = CashRebate(0.8)

        return cs or CashNormal()


def btnOk_Click(total, price, numbers, alg):
    # 选择策略
    cashsuper = CashFactory.createCashAccept(alg)
    totalPrice = cashsuper.acceptCash(price * numbers)

    total += totalPrice
    print("单价: %s, 数量: %s, 合计: %s" % (price, numbers, totalPrice))
    return total


# -------------------------------------------------------------------

class Strategy(abc.ABC):
    @abc.abstractclassmethod
    def algorithmInterface(self):
        """算法方法"""
        raise NotImplementedError


class ConcreteStrategyA(Strategy):
    def algorithmInterface(self):
        print("算法A实现方法")


class ConcreteStrategyB(Strategy):
    def algorithmInterface(self):
        print("算法B实现方法")


class ConcreteStrategyC(Strategy):
    def algorithmInterface(self):
        print("算法C实现方法")


class Context(object):
    """上下文

    维护一个对Strategy对象的引用
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def contextInterface(self):
        self._strategy.algorithmInterface()


# ------------------------------------------------------------------

class CashContext(object):
    def __init__(self, csuper: CashSuper):
        self._cs = csuper

    def getResult(self, money):
        return self._cs.acceptCash(money)


def client8(total, price, numbers, alg):
    if alg == "满３００减５０":
        cc = CashContext(CashReturn(300, 50))
    elif alg == "8折":
        cc = CashContext(CashRebate(0.8))
    else:
        cc = CashContext(CashNormal())

    totalPrice = cc.getResult(price * numbers)
    total += totalPrice
    print("单价: %s, 数量: %s, 合计: %s" % (price, numbers, totalPrice))
    return total


# --------------------------------------------------------
class CashContext2(object):
    def __init__(self, alg):
        self._strategy = self._getStrategy(alg)

    def _getStrategy(self, alg):
        if alg == "满３００减５０":
            cs = CashReturn(300, 50)
        elif alg == "8折":
            cs = CashRebate(0.8)
        else:
            cs = CashNormal()
        return cs

    def getResult(self, money):
        return self._strategy.acceptCash(money)


def client9(total, price, numbers, alg):
    cc = CashContext2(alg)
    totalPrice = cc.getResult(price * numbers)
    total += totalPrice
    print("单价: %s, 数量: %s, 合计: %s" % (price, numbers, totalPrice))
    return total


if __name__ == "__main__":
    # print(btnOk_Click(0, 20, 5, "8折"))
    print(client9(0, 50, 9, "8折"))
