# 第2章 策略模式

标签： `设计模式`

---

## 商场收银软件
```
def btnOk_Click(total, price, numbers):
    totalPrice = price * numbers
    total += totalPrice
    print("单价: %s, 数量: %s, 合计: %s" % (price, numbers, totalPrice))
    return total
```
A: 我现在要求商场对商品搞活动，所有的商品打八折.
B: 那不就是在totalPrices后面乘以0.8吗？
A: 难道商场活动结束，不打折了，你还要再改一次代码，然后再用改后的程序去把所有机器全部安装一次吗？再说还有打五折的情况？
B: 通过下拉框解决.

## 2.2 增加打折
```
def btnOk_Click(total, price, numbers, alg):
    # 选择策略
    if alg == 0:
        totalPrice = price * numbers
    elif alg == 1:
        totalPrice = price * numbers * 0.8
    elif alg == 2:
        totalPrice = price * numbers * 0.7
    elif alg == 3:
        totalPrice = price * numbers * 0.5

    total += totalPrice
    print("单价: %s, 数量: %s, 合计: %s" % (price, numbers, totalPrice))
    return total
```
A: 灵活性好多了，不过重复代码很多，像Convert.ToDouble()就写了8遍，而且4个分支要执行的语句除了打折多少以外几乎没有差别，应该考虑重构一下.重点是，有新的需求，满300返100的活动，怎么办？
B: 根据需求，子类有几个写几个.
A: 我要漫300送80，难道再去加子类？你不想想这当中有哪些是相同的，哪些是不同的.

## 2.3 简单工厂实现
B: 打折基本相同，只要个初始化参数就可以了.满几送几，需要两个参数.
A: 面向对象编程，并不是类越多也好，类的划分是为了封装，但分类的基础是抽象，具有相同属性和功能的对象的抽象集合才是类.打一折和打九折只是形式不同，抽象分析出来，所有的算法都是一样的，所有打折算法应该是个类.

代码结构图:
 ![11](http://h.hiphotos.baidu.com/image/pic/item/5882b2b7d0a20cf40e7ae3667c094b36adaf99a4.jpg)
 
现金收取父类
```
class CashSuper(abc.ABC):
    @abc.abstractclassmethod
    def acceptCash(self, money):
        """收取现金，参数为原价，返回为当前价"""
        raise NotImplementedError
```
正常收费子类
```
class CashNormal(CashSuper):
    """正常收款"""

    def acceptCash(self, money):
        return money
```
打折收费类
```
class CashRebate(CashSuper):
    """打折类"""

    def __init__(self, rebate=1.0):
        self._rebate = rebate

    def acceptCash(self, money):
        return money * self._rebate
```
返利收费子类
```
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
```
现金收费工厂类:
```
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
```
客服端:
```
def btnOk_Click(total, price, numbers, alg):
    # 选择策略
    cashsuper = CashFactory.createCashAccept(alg)
    totalPrice = cashsuper.acceptCash(price * numbers)

    total += totalPrice
    print("单价: %s, 数量: %s, 合计: %s" % (price, numbers, totalPrice))
    return total
```
A: 这是如果要增加满100积分10点？
B: 收费对象生成工厂里增加满100积分10点的分支条件，再到界面稍加修改.
A: 简单工厂模式虽然也能解决这个问题，但是这个模式只是解决对象的创建问题，而且由于工厂本身包括了所有的收费方式，商场是可能经常性地改打折额度和返利额度，每次维护或扩展收费方式都要改动这个工厂，以至代码重新编译部署.**面对算法的时常变动，应该有更好的方法.**

## 2.4 策略模式
> 它定义了算法家族，分别封装起来，让它们之间可以互相替换，此模式让算法的变化，不会影响到使用算法的客服.

商场收银时如何促销，用打折还是返利，其实就是一些算法，用工厂来生成算法对象，这没有错，但是算法本身只是一种策略，最重要的是**这些算法是随时都有可能互相替换的，这就是变化点，而封装变化点是我们面向对象的一种重要的思维方式.**

策略模式的结构图和基本代码:
![策略模式](http://c.hiphotos.baidu.com/image/pic/item/91529822720e0cf3d5bc4f420046f21fbe09aa3b.jpg)


抽象算法类
```
class Strategy(abc.ABC):
    @abc.abstractclassmethod
    def algorithmInterface(self):
        """算法方法"""
        raise NotImplementedError
```
具体算法A
```
class ConcreteStrategyA(Strategy):
    def algorithmInterface(self):
        print("算法A实现方法")
```
具体算法B
```
class ConcreteStrategyB(Strategy):
    def algorithmInterface(self):
        print("算法B实现方法")
```
具体算法C
```
class ConcreteStrategyC(Strategy):
    def algorithmInterface(self):
        print("算法C实现方法")
```
上下文(用一个ConcreteStrategy来配置，维护一个对Strategy对象的引用)
```
class Context(object):
    """上下文

    维护一个对Strategy对象的引用
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def contextInterface(self):
        self._strategy.algorithmInterface()
```
客服端:
```
if __name__ == "__main__":
    context = Context(ConcreteStrategyA())
    context.contextInterface()  # 算法A实现方法

    context = Context(ConcreteStrategyB())
    context.contextInterface()  # 算法B实现方法

    context = Context(ConcreteStrategyC())
    context.contextInterface()  # 算法C实现方法
```
## 2.5 策略模式实现
代码结构图:
![结构图3](http://f.hiphotos.baidu.com/image/pic/item/5366d0160924ab180a18ec8e3ffae6cd7b890b78.jpg)

CashContext:
```
class CashContext(object):
    def __init__(self, csuper: CashSuper):
        self._cs = csuper

    def getResult(self, money):
        return self._cs.acceptCash(money)
```
客服端
```
def btnOk_Click(total, price, numbers, alg):
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
```
B: 在客服端去判断用哪一个算法？
A: 有没有好办法，把这个判断的过程从客服端移走呢？
A: 难道简单工厂就一定是一个单独的类吗？难道不可以与策略模式的Context结合？(与Context关联度比较高，应将代码转移到Context类中.实例化算法，将其加入到Context中，其后的计算都是调用Context.)
## 2.6 策略与简单工厂模式
改造后的CashContext:
```
class CashContext(object):
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
```
客服端:
```
def client9(total, price, numbers, alg):
    cc = CashContext(alg)
    totalPrice = cc.getResult(price * numbers)
    total += totalPrice
    print("单价: %s, 数量: %s, 合计: %s" % (price, numbers, totalPrice))
    return total
```

不同:
简单工厂模式写法:
```
csuper = CashFactory.createCashAccept(alg);
...=csuper.GetResult(...)
```
策略模式和简单工厂结合:
```
csuper = new CashContext(alg);
...=csuper.GetResult(...);
```
B: 你的意思是，简单工厂模式我需要让客服端认识两个类，CashSuper和CashFactory，而策略模式与简单工厂结合的用法，客服端就只需要认识一个类CashContext就可以了.耦合更加降低.
A: 这使得具体的收费算法彻底地与客服端分离.
##2.7 策略模式解析
* 策略模式是一种定义一系列算法的方法(打几折)，从概念上来看，所有这些算法完成的都是相同的工作，只是实现不同，它们可以以相同的方式调用相同所有的算法，减少了各种算法类与使用算法类之间的耦合.
* 策略模式的Strategy层次为Context定义了一系列的可供重用的算法或行为.继承有助于析取出这些算法中的公共功能.
* 公共的功能就是获取计算费用的结果的GetResult，这使得算法间有了抽象的父类CashSuper.
* 简化了单元测试，因为每个算法都有自己的类，可以通过自己的接口单独测试.互补影响.
* 客服端中的switch分支，这也是正常的.因为，当不同的行为堆砌在一个类中时，就很难避免使用条件语句来选择合适的行为.将这些行为封装在一个个独立的Strtegy类中，可以在使用这些行为的类中消除条件语句.在客服端代码中消除条件语句，避免大量判断(虽然转移到CashContext中)，这也是非常重要的进展.
* 策略模式就是用来封装算法的，但是在实践中.我们发现可以用它来封装几乎任何类型的规则，只要在分析过程中听到**需要在不同时间应用不同的业务规则，就可以考虑使用策略模式处理这个变化的可能性**
* 在CashContext里还是用到了switch，也就是说，如果我们需要增加一种算法，你必须要更改CashContext中的switch代码.
* 面对同样的需求，当然是改动越小越好.
