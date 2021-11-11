# coding:utf-8
# 《python金融编程快速入门与项目实操》练习
# 投资组合问题


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as sco
import scipy.interpolate as sci
import akshare as ak
import run


# 获取数据
def get_data():
    codes = ["601939", "600104", "600519"]
    data = pd.DataFrame()
    start = "20160616"
    end = "20160718"
    dates = []
    for code in codes:
        stock_data = ak.stock_zh_a_hist(symbol = code, start_date = start, end_date = end)
        # print(code, stock_data.head())
        data[code] = stock_data["收盘"]/stock_data["收盘"].shift(1) - 1
    data["日期"] = stock_data.日期
    data.set_index(keys = "日期", inplace = True)
    data.dropna(inplace = True)
    return data
    
    
# 投资权重模拟
# 通过10000次模拟，产生各种可能的投资组合
def simulate(data):
    prets = []
    pvols = []
    I = 10000
    rets = data.values
    # print(rets)
    num = len(data.columns)
    rets_mean_year = data.mean()*252
    rets_cov_year = data.cov()*252
    # print(rets_mean_year, rets_cov_year)
    
    for p in range(I):
        weights = np.random.random(num)
        weights /= np.sum(weights)
        prets.append(np.sum(rets_mean_year*weights))
        pvols.append(np.sqrt(np.dot(weights.T, np.dot(rets_cov_year, weights))))
        
    prets = np.array(prets)
    pvols = np.array(pvols)
    draw_simulate(prets, pvols, "simulate.jpg")
    return (prets, pvols, weights)
    
    
# 确定投资组合的有效前沿
def front(data, prets, pvols, weights):
    # 最优组合
    def func_stats(weights, rets):
        weights = np.array(weights)
        pret = np.sum(data.mean()*weights)*252
        # 投资组合的收益率
        pvol = np.sqrt(np.dot(weights.T, np.dot(data.cov()*252, weights)))
        # 投资组合的标准差
        return np.array([pret, pvol, pret/pvol])
        
    def func_min_sr(weights, rets):
        return func_stats(weights, rets)[2]
        
    def func_min_variance(weights, rets):
        return func_stats(weights, rets)[1]**2
        
    def func_min_vol(weights, rets):
        return func_stats(weights, rets)[1]
        
    # 求最大收益波动率比率
    num = len(data.columns)
    rets = data.values
    cons = ({"type":"eq", "fun":lambda x:1-np.sum(x)})
    bnds = tuple((0,1) for x in range(num))
    opts = sco.minimize(lambda x: func_min_sr(x, rets), num*[1.0/num], method = "SLSQP", bounds = bnds, constraints = cons)
    opt_sr_weights = opts["x"].round(3)
    
    ret_min = min(prets)
    ret_max = max(prets)
    vol_min = min(pvols)
    ind_min_vol = np.argmin(pvols)
    ret_start = prets[ind_min_vol]
    
    trets = np.linspace(ret_start, ret_max, 100)
    tvols = []
    for tret in trets:
        cons = (
            {
                "type":"eq",
                "fun":lambda x: func_stats(x, rets)[0] - tret
            },
            {
                "type":"eq",
                "fun":lambda x: 1-np.sum(x) 
            }
        )
        res = sco.minimize(lambda x: func_min_sr(x, rets), num*[1.0/num], method = "SLSQP", bounds = bnds, constraints = cons)
        tvols.append(res["fun"])
    tvols = np.array(tvols)
    draw_simulate(trets, tvols, "front.jpg", marker = "x")
    return tvols, trets
    
    
# 画出模拟结果
@run.change_dir
def draw_simulate(prets, pvols, name, marker = "o"):
    plt.figure(figsize = (8, 5))
    plt.scatter(pvols, prets, c = prets/pvols, marker = marker)
    plt.grid(True)
    plt.xlabel("标准差(风险)")
    plt.ylabel("期望收益率")
    plt.colorbar(label = "期望收益率/标准差")
    plt.savefig("./output/" + name)


# 加入无风险资产后的最优资产组合
@run.change_dir
def risk_free(data, prets, pvols, tvols, trets):
    ind = np.argmin(tvols)
    evols = np.sort(tvols[ind:])
    erets = trets[ind:]
    print(len(evols), len(erets))
    tck = sci.splrep(evols, erets)
    
    def func_ef(x, tck):
        return sci.splev(x, tck, der = 0)
        
    def func_def(x, tck):
        return sci.splev(x, tck, der = 1)
        
    def func_equation(p, tck, rf = 0.05):
        eq1 = rf - p[0]
        eq2 = rf + p[1]*p[2] - func_ef(p[2], tck)
        eq3 = p[1] - func_def(p[2], tck)
        return eq1, eq2, eq3
        
    opt = sco.fsolve(lambda s: func_equation(s, tck), [0.05, 0.2, 0.2], xtol = 1e-05)
        
    # 画图
    plt.figure(figsize = (8, 4))
    # 可行域
    plt.scatter(pvols, prets, c = (prets - 0.01)/pvols, marker = "o")
    # 有效前沿
    plt.plot(tvols, trets, "g", lw = 2.0)
    # 切点
    plt.plot(opt[2], func_ef(opt[2], tck), "r*")
    # 市场组合
    cx = np.linspace(0.0, max(pvols))
    plt.plot(cx, opt[0] + opt[1]*cx, lw = 1.5)
    # 图像背景
    plt.grid(True)
    plt.axhline(0, color = "k", ls = "--", lw = 2.0)
    plt.axvline(0, color = "k", ls = "--", lw = 2.0)
    plt.xlabel("标准差(风险)")
    plt.ylabel("期望收益率")
    plt.savefig("./output/best.jpg")
    
    # 最优组合的资产配置
    rets = data.values
    tpr = func_ef(opt[2], tck)
    cons = (
            {
                "type":"eq",
                "fun":lambda x: func_stats(x, rets)[0] - tpr
            },
            {
                "type":"eq",
                "fun":lambda x: 1-np.sum(x) 
            }
        )
    num = len(data.columns)
    bnds = tuple((0, 1) for x in range(num))
    
    # 最优组合
    def func_stats(weights, rets):
        weights = np.array(weights)
        pret = np.sum(data.mean()*weights)*252
        # 投资组合的收益率
        pvol = np.sqrt(np.dot(weights.T, np.dot(data.cov()*252, weights)))
        # 投资组合的标准差
        return np.array([pret, pvol, pret/pvol])
        
    def func_min_sr(weights, rets):
        return func_stats(weights, rets)[2]
        
    def func_min_variance(weights, rets):
        return func_stats(weights, rets)[1]**2
        
    def func_min_vol(weights, rets):
        return func_stats(weights, rets)[1]

    res = sco.minimize(lambda x: func_min_vol(x, rets), num*[1.0/num], method = "SLSQP", bounds = bnds, constraints = cons)
    
    optwei = []
    optwei.append(res.x.round(3))
    print(optwei)
    


if __name__ == "__main__":
    data = get_data()
    # print(data.head())
    prets, pvols, weights = simulate(data)
    tvols, trets = front(data, prets, pvols, weights)
    risk_free(data, prets, pvols, tvols, trets)