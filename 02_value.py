# coding:utf-8
# 《python金融编程快速入门与项目实操》练习
# 计算资金的时间价值


def value():
    pv = 100 # 现值
    rate = 0.1 # 折现利率
    T = 10 # 投资期限
    
    fv = pv * (1 + rate)**T
    print("终值为:", fv)
    
    fv = 100 # 终值
    pv = fv / (1 + rate)**T 
    print("现值为:", pv)
    
    # 已知报价利率计算有效年利率
    sar = 0.03 # 报价利率
    m = 12 # 付息次数
    ear = (1 + sar/m)**m - 1
    print("有效年利率为:", ear)
    
    
if __name__ == "__main__":
    value()