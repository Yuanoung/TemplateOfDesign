# 第1章 简单工厂模式

标签（空格分隔）： 设计模式

---
## 1.1 面试受挫
```
# 面试受挫
class Program(object):
    def __init__(self):
        pass

    def getResult(self):
        a = int(input("请输入数字:\n>>> "))
        c = input("请输入运算符:\n>>> ")
        b = int(input("请输入另一个数字:\n>>> "))

        if c == "+":
            r = a + b
        elif c == "-":
            r = a - b
        elif c == "*":
            r = a * b
        else:
            r = a / b
        print("运算结果为： ", r)
```
##1.2 初学者代码毛病
* `string A; string B; string C`这样的命名是非常不规范的.
* 判断分支，这样的写法，意味着每个条件都要做判断，等于计算机做了三次无用功.
* 如果除数时，客服端输入了0怎么办，如果用户输入的是字符符号而不是数字怎么办.

##1.3 代码规范
```
class Program(object):
    def __init__(self):
        pass

    def getResult(self):
        a = int(input("请输入数字:\n>>> "))
        c = input("请输入运算符:\n>>> ")
        b = int(input("请输入另一个数字:\n>>> "))
        
        if c == "+":
            r = a + b
        elif c == "-":
            r = a - b
        elif c == "*":
            r = a * b
        else:
            if b == 0:
                print("除数不能为0，请重新输入")
                exit(0)
            else:
                r = a / b
        print("运算结果为： ", r)
```
##1.4 面向对象编程
碰到问题就直觉地用计算机能够理解的逻辑来描述和表达待解决的问题及求解过程.这其实是计算机的方式思考，这并没有错.但是这样的思维却使得我们的程序只为满足实现当前的需求，程序不容易维护，不容易扩展，更不容易复用.从而达不到高质量代码的要求.
##1.5 活字印刷，面向对象
- 在这之前，要修改，必须重刻；要加字，必须重刻；要重新排列，必须重刻；印完该书，此版毫无价值.
- 活字印刷:
1) 要改，只需要改要改之字，**可维护**；
2) 重复使用，**可复用**；
3) 加字，另刻字加入即可，**可扩展**；
4) 竖排横排，将活字移动即可，**灵活性好**.

##1.6 面向对象的好处
要改需求，更改最初的想法的事件，才逐渐明白当中的道理.
开始通过封装，继承，多态把程序的耦合性降低，用设计模式使得程序更加的灵活，容易修改，并且易于复用.

##1.7 复制与复用
复制，因为当你的代码中重复的代码多到一定程度，维护的时候，可能就是一场灾难.越大的系统，这种方式带来的问题越严重，编程有一原则，就是用尽可能的办法去避免重复.**想想看，有哪些是和控制台无关，而哪些只是和计算器有关的**.
##1.8 业务的封装
让业务逻辑与界面逻辑分开，让它们之间的耦合度下降.

Operation运算类:
```
class Operation(object):
    @staticmethod
    def getResult(numberA, op, numberB):  
        # 这里就单个函数更简单，但是还是用类来实现，
        if op == "+":
            return numberA + numberB
        elif op == "-":
            return numberA - numberB
        elif op == "*":
            return numberA * numberB
        else:
            return numberA / numberB
```
客服端代码:
```
if __name__ == "__main__":
    numberA = int(input("请输入数字:\n>>> "))
    op = input("请输入运算符:\n>>> ")  # 这里略过对操作符的
    numberB = int(input("请输入另一个数字:\n>>> "))
    
    try:
        print(Operation(numberA, op, number B)
    except ZeroDivisionError:
        return "除数不能为0"
```
##1.9 紧耦合vs.松耦合
A: 如何做到很灵活的可修改和可扩展？比如说增加一个平方根运算，如何改？
B: 只需要修改`Operation`类就可以了，在switch中加一个分支就行了.
A: 问题是你要加一个平方根运算，却需要让加减乘除的运算都得来参与编译.
B: 我应该把加减乘除等运算分离，修改其中一个不影响另外的几个，增加运算算法也不影响其他代码？
A: 如何用继承和多态，你应该有感觉了.

Operation运算类:
```
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
```
B: 我如何让计算器知道我希望用哪一个算法呢？

##1.10 简单工厂模式
A: 你现在的问题就是如何去实例化对象的问题，到底要实例化谁，将来会不会增加实例化的对象，比如增加开根运算，这是很容易变化的地方，应该考虑用一个单独的类做这个创造实例的过程，这就是工厂.

简单运算工厂类:
```
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
```
客服端代码:
```
if __name__ == "__main__":
    numberA = int(input("请输入数字:\n>>> "))
    op = input("请输入运算符:\n>>> ")  # 这里略过对操作符的判断
    numberB = int(input("请输入另一个数字:\n>>> "))

    opCls = OperationFactory.createOperation(op)
    operation = opCls(numberA, numberB)
    print(operation.getResult())
```
A: 如果有一天我们需要更改加法运算，我们只需要改哪里？
B: 改OperationAdd就可以了.
A: 增加运算？
B: 只要增加相应的运算子类就可以了.还要去修改运算类工厂，在switch中增加分支.

这几个类的结构图:
![结构图](http://h.hiphotos.baidu.com/image/pic/item/7e3e6709c93d70cfa41b89b4f2dcd100bba12ba1.jpg)
## 1.11 UML类图
![UML类图图示样例](http://b.hiphotos.baidu.com/image/pic/item/6c224f4a20a4462310b388db9222720e0cf3d709.jpg)
编程是一门技术，更是一门艺术，不能只满足于写完代码运行结果正确就完事了，时常考虑如何让代码更加简练，更加容易维护，容易扩展和复用，只有这样才能真正提高.


  [1]: http://h.hiphotos.baidu.com/image/pic/item/7e3e6709c93d70cfa41b89b4f2dcd100bba12ba1.jpg
  [2]: http://b.hiphotos.baidu.com/image/pic/item/6c224f4a20a4462310b388db9222720e0cf3d709.jpg