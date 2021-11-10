# coding:utf-8
# 《python金融编程快速入门与项目实操》练习
# 期权定价模型


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import datetime


class call_option:
    def __init__(self, S0, K, Pdate, Mdate, r, sigma):
        self.S0 = S0
        self.K = K
        self.Pdate = Pdate
        self.Mdate = Mdate
        self.r = r
        self.sigma = sigma
        
    # 计算期权到期时间
    def ttm(self):
        if self.Pdate > self.Mdate:
            raise ValueError("错误:合约起始日迟于到期日!")
        else:
            return (self.Mdate - self.Pdate).days/365
            
    def d1(self):
        ttm = self.ttm()
        return (np.log(self.S0/self.K) + (self.r+0.5*self.sigma**2)*ttm)/(self.sigma*np.sqrt(ttm))
        
    def d2(self):
        ttm = self.ttm()
        return (np.log(self.S0/self.K) + (self.r-0.5*self.sigma**2)*ttm)/(self.sigma*np.sqrt(ttm))
        
    def pv_value(self):
        d1 = self.d1()
        d2 = self.d2()
        T = self.ttm()
        value = (self.S0*stats.norm.cdf(d1, 0.0, 1.0) - self.K*np.exp(-self.r*T)*stats.norm.cdf(d2, 0.0, 1.0))
        return value
        
    def delta(self):
        return stats.norm.cdf(self.d1(), 0.0, 1.0)
        
    def vega(self):
        return self.S0*stats.norm.pdf(self.d1(), 0.0, 1.0)*np.sqrt(self.ttm())
        
    def gamma(self):
        return stats.norm.pdf(self.d1(), 0.0, 1.0)/(self.S0*self.sigma*np.sqrt(self.ttm()))
        
        
def option_graph(name):
    plt.figure(figsize = (8, 5))
    plt.grid(True)
    plt.title(name)
    
    
def draw(S0, K, pricing_date, maturity_date, r, sigma):
    K1 = np.linspace(2.25, 2.65, 80)
    c_eurl = call_option(S0, K1, pricing_date, maturity_date, r, sigma)
    print(c_eurl.pv_value())
    option_graph("pv")
    plt.plot(K1, c_eurl.pv_value())
    plt.savefig("k_pv.jpg")
    option_graph("delta")
    plt.plot(K1, c_eurl.delta())
    plt.savefig("k_delta.jpg")
    option_graph("gamma")
    plt.plot(K1, c_eurl.gamma())
    plt.savefig("k_gamma.jpg")
    option_graph("vega")
    plt.plot(K1, c_eurl.vega())
    plt.savefig("k_vega.jpg")
        
        
def main():
    pricing_date = datetime.datetime(2018, 11, 28)
    maturity_date = datetime.datetime(2019, 1, 23)
    S0 = 2.47
    K = 2.5
    r = 0.04
    sigma = 0.2
    
    c_eur = call_option(S0, K, pricing_date, maturity_date, r, sigma)
    print(c_eur.pv_value())
    print(c_eur.delta())
    print(c_eur.vega())
    print(c_eur.gamma())
    
    draw(S0, K, pricing_date, maturity_date, r, sigma)
    


if __name__ == "__main__":
    main()