# coding:utf-8
# 将程序上传到服务器上执行
import os
import sys
from functools import wraps
import time


# 两个常用的工具函数，装饰器
# 工具函数，在上传到服务器上运行时改变当前目录
def change_dir(func):
    @wraps(func)
    def change(*args, **kwargs):
        oldpath = os.getcwd()
        newpath = "/home/code/"
        os.chdir(newpath)
        r = func(*args, **kwargs)
        os.chdir(oldpath)
        return r
    return change
    
    
# 工具函数，计算函数运行时间    
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{}的运行时间为 : {}秒'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper


# 运行代码前准备
def before_run(user, server):
    # 清除服务器代码目录里所有源文件以及输出目录中的文件
    s = "ssh " + user + "@" + server + " \"sudo rm -rf ~/code/*\""
    # print("测试1", s)
    os.system(s)
    s = "ssh " + user + "@" + server + " \"sudo rm -f ~/code/output/*\""
    # print("测试2", s)
    os.system(s)
    # 将本地目录所有文件上传至容器
    s = "scp -r ./* " + user + "@" + server + ":~/code"
    # print("测试3", s)
    os.system(s)
    # 创建输出目录
    s = "ssh " + user + "@" + server + " \"sudo mkdir ~/code/output\""
    # print("测试4", s)
    os.system(s)
    # s = "scp -r ./*.csv " + user + "@" + server + ":~/code"
    # os.system(s)
    # 更改服务器容器里的当前目录
    s = "ssh root@" + server +  " -p 2222 \"cd /home/code\""
    os.system(s)
    
    
# 运行完成后的后续操作
def after_run(user, server):
    # 将代码目录里所有输出文件传回
    s = "scp -r " + user +"@" + server + ":~/code/output/* ./output/"
    # print("测试5", s)
    os.system(s)


# 上传代码至服务器并运行
def run(gpus, user, server):
    # 上传本目录所有文件再执行指定文件
    if gpus == "all":
        before_run(user, server)
        # 运行指定代码
        s = "ssh root@" + server +  " -p 2222 \"python -u /home/code/" + sys.argv[2] + "\""
        # print("测试4", s)
        print("正在运行代码……\n")
        os.system(s)
        after_run(user, server)
    elif gpus == "copy":
        after_run(user, server)
    # 用pytest执行单元测试
    elif gpus == "test":
        before_run(user, server)
        # 运行指定代码
        arg_len = len(sys.argv)
        if arg_len == 3:
            s = "ssh root@" + server +  " -p 2222 \"/opt/conda/bin/pytest -v /home/code/" + sys.argv[2] + "\""
        # elif arg_len == 2:
        #     s = "ssh root@" + server +  " -p 2222 \"/opt/conda/bin/pytest -v\""
        else:
            print("输入有误!")
            return
        print("测试4", s)
        print("正在测试代码……\n")
        os.system(s)
        after_run(user, server)
    else:
        print("输入有误，格式: python run.py all/copy/test filename.py 其中filename.py为要运行/测试的源文件。")
        
        
# 主函数
def main():
    gpus = sys.argv[1]
    # 读取服务器IP地址，自己编辑serverIP.txt去
    with open("serverIP.txt", "rt") as f:
        server_list = f.readlines()
    for s in server_list:
        s = s.replace('\n', '').replace('\r', '')
        # print(s)
        if s[0] != "#":
            res = s.split("@")
            username = res[0]
            server = res[1]
            # print("测试", username, server)
            # input("按任意键继续")
            run(gpus, username, server)
            return    


if __name__ == "__main__":
    main()
        
    
