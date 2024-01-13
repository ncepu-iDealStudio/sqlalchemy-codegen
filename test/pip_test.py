# coding: utf-8
# @Author : lryself
# @Date : 2022/4/6 11:14
# @Software: PyCharm
import os

if __name__ == '__main__':
    os.system("rd /s/q results")
    # os.mkdir("results")
    os.system("pip install .")
    os.system('sqlalchemy-codegen mysql+pymysql://dev:123456@127.0.0.1:3306/codegen_db?charset=utf8mb4 --outdir "results" --models_layer --controller_layer --flask')