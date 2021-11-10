# coding:utf-8
# 《python金融编程快速入门与项目实操》练习
# 汇率换算
# 输入汇率和金额及币种，输出换算金额


# 测试换算程序
def test_currency():
    assert currency(6.0, "3.0CNY") == "0.5USD"
    assert currency(6.0, "5.0USD") == "30.0CNY"
    assert currency(-3.0, "2.0USD") == "汇率需大于0"
    assert currency(3.0, "-2.0CNY") == "金额需大于0"
    assert currency(3.0, "5.0USA") == "货币单位错误，需为CNY或USD"
    assert currency(6.0, "6.5DUSA") == "输入的金额不是数字"


# 货币兑换程序
def currency(rate, amount):
    res = judge(rate, amount)
    if res != "OK":
        return res
    curr = amount[-3:]
    money = eval(amount[0:-3])
    if curr == "CNY":
        return str(money / rate) + "USD"
    elif curr == "USD":
        return str(money * rate) + "CNY"
        
        
# 测试判断程序
def test_judge():
    assert judge(6.0, "3.0CNY") == "OK"
    assert judge(6.0, "5.0USD") == "OK"
    assert judge(-3.0, "2.0USD") == "汇率需大于0"
    assert judge(3.0, "-2.0CNY") == "金额需大于0"
    assert judge(3.0, "5.0USA") == "货币单位错误，需为CNY或USD"
    assert judge(6.0, "6.5DUSA") == "输入的金额不是数字"
        
        
# 判断参数是否合法
def judge(rate, amount):
    if rate <= 0.0:
        return "汇率需大于0"
    curr = amount[-3:]
    if isdigit(amount[0:-3]) == False:
        return "输入的金额不是数字"
    if curr != "CNY" and curr != "USD":
        return "货币单位错误，需为CNY或USD"
    money = eval(amount[0:-3])
    if money <= 0.0:
        return "金额需大于0"
    return "OK"
        
        
# 测试字符串判断函数
def test_isdigit():
    assert isdigit("666") == True
    assert isdigit("666.66") == True
    assert isdigit("-555.66") == True
    assert isdigit("655.54+") == False
    assert isdigit("-544gf") == False
        
        
# 判断字符串是否为数字
def isdigit(money):
    if money.count('.') == 1:
        left = money.split(".")[0]
        right = money.split(".")[1]
        if right.isdigit():
            if left.count("-") == 1 and left.startswith("-"):
                num = left[1:]
                if num.isdigit():
                    return True
            elif left.isdigit():
                return True
    elif money.count('.') == 0:
        return money.isdigit()
    return False
        
        
# 输入程序
def get_input():
    rate = float(input("请输入汇率:"))
    amount = input("请输入换算金额，以CNY/USD结尾:")
    return rate, amount
    
    
if __name__ == "__main__":
    datas = get_input()
    result = currency(datas[0], datas[1])
    print("换算结果为:", result)
