# 面试受挫
class Program(object):
    def __init__(self):
        pass

    def main(self):
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


if __name__ == "__main__":
    program = Program()
    program.main()
