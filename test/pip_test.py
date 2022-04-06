# coding: utf-8
# @Author : lryself
# @Date : 2022/4/6 11:14
# @Software: PyCharm
import os

if __name__ == '__main__':
    os.system("rd /s/q results")
    # os.mkdir("results")
    os.system("pip install .")
    os.system('flask-sqlalchemy-codegen mysql+pymysql://paperreview_dev:paperreview_dev@139.9.128.8:3306/paperreview?charset=utf8mb4 --outdir "results" --models_layer --controller_layer --flask')