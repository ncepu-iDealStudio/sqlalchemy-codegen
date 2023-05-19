## sqlalchemy-codegen

#### 功能说明
这是一个能够基于sqlalchemy ORM框架，通过命令行的方式运行，可以自动生成相应的实体层(Model)和控制器层(controller)代码的工具；
支持针对整个数据库来生成，也可以针对特定的表来生成相应的代码；同时也支持基于Flask框架来生成相应的代码；

代码仓库和相关地址：

github:https://github.com/ncepu-iDealStudio/sqlalchemy-codegen

gitee:https://gitee.com/ncepu-bj/sqlalchemy-codegen

document:https://idealstudio-ncepu.yuque.com/docs/share/b5dcc5ff-fcba-4efd-8955-faeba859bfcf

pypi:https://pypi.org/project/sqlalchemy-codegen/

本项目fork自 [flask-sqlacodegen](https://github.com/ksindi/flask-sqlacodegen) 作者： Kamil Sindi. 基于version 1.1.8.
在此基础上，我们做了大量的改进工作；

项目特性以及所做的改进工作:
* 支持生成控制器层，实现对基本实体的CRUD操作.
* 支持生成实体层文件夹，并将每个表对应的实体文件分离出来单独存放.
* 使用`sqlalchemy-codegen` 代替 `flask-sqlacodegen`.
* 支持Flask-SQLAlchemy语法，通过使用`--flask`选项.
* 支持表之间的反向引用(backrefs)关系. 当您不需要backrefs时，`--nobackref`选项依然可用。
* backrefs的命名采用snake_case (与CamelCase相反) ，如果是多对一或多对多是使用 [inflect](https://pypi.python.org/pypi/inflect).
* 主键关联是显式的.
* 如果数据库字段有默认值，则将其设置为“FetchValue（）”，无需要确定该值是什么。原始代码没有在我的设置中配置正确的数据库默认值
* 通过`--ignore-cols` 选项，可以在生成关联表时忽略特殊列。原始代码要求所有列都是外键，以便生成关联表；Example: `--ignore-cols id,inserted,updated`.
* 添加支持 `--notables` 选项，支持仅仅生成model classes,即便是关联表


#### 如何贡献代码
感谢您参与贡献代码，可通过以下方式获取代码:
```sh
git clone https://gitee.com/ncepu-bj/sqlalchemy-codegen
python -m venv env
pip install -r requirements.txt
python -m codegen.main mysql+pymysql://<username>:<password>@<database-ip>:<port>/<database-name> --flask --models_layer --controller_layer --outdir ddist[--tables <tablenames>] [--notables] 

```

#### 安装使用说明

使用pip安装:
```
pip install sqlalchemy-codegen
```

使用其它方式安装:
```
git clone https://gitee.com/ncepu-bj/sqlalchemy-codegen.git
cd sqlalchemy-codegen/
python setup.py install

使用方式(一般情形):

```
sqlalchemy-codegen mysql+pymysql://root:password@ip:port/database  --models_layer --controller_layer --outdir dist
'''

使用方式(基于flask框架):

'''
sqlalchemy-codegen mysql+pymysql://root:password@ip:port/database --flask --models_layer --controller_layer --outdir dist
'''

如:
'''
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --flask --models_layer --controller_layer --outdir dist
'''