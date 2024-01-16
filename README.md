## sqlalchemy-codegen

#### features
This is a tool that can generate corresponding Model and controller layer codes based on the sqlalchemy ORM framework through command-line operation. It supports generating codes for the entire database or for specific tables. Additionally, it supports generating codes based on the Flask framework.

Code repository and related addresses: 
github:https://github.com/ncepu-iDealStudio/sqlalchemy-codegen;

gitee:https://gitee.com/ncepu-bj/sqlalchemy-codegen;

document:https://idealstudio-ncepu.yuque.com/docs/share/b5dcc5ff-fcba-4efd-8955-faeba859bfcf;

pypi:https://pypi.org/project/sqlalchemy-codegen/


What's new and different:
* Support python3.12 and sqlacodegen3.0.0rc3 SQLAlchemy2.0.25.
* Support for generate controller layer.
* Support for generate Model layer include many model py files.
* Support for Flask-SQLAlchemy syntax using `--flask` option.
* Defaults to generating backrefs in relationships. `--nobackref` still included as option in case backrefs are not wanted. 
* Naming of backrefs is class name in snake_case (as opposed to CamelCase) and is pluralized if it's Many-to-One or Many-to-Many using [inflect](https://pypi.python.org/pypi/inflect).
* Primary joins are explicit.
* If column has a server_default set it to `FetchValue()` instead of trying to determine what that value is. Original code did not set the right server defaults in my setup.
* `--ignore-cols` ignores special columns when generating association tables. Original code requires all columns to be foreign keys in order to generate association table. Example: `--ignore-cols id,inserted,updated`.
* Uses the command `flask-sqlacodegen` instead of `sqlacodegen`.
* Added support for `--notables` to only generate model classes, even for association tables

## Install

With pip:
```sh
pip install sqlalchemy-codegen
```

Without pip:
```sh
git clone https://gitee.com/ncepu-bj/sqlalchemy-codegen.git
cd sqlalchemy-codegen/
python setup.py install
```

For contributing:
```sh
git clone https://gitee.com/ncepu-bj/sqlalchemy-codegen
python -m venv env
pip install -r requirements.txt
python -m codegen.main mysql+pymysql://<username>:<password>@<database-ip>:<port>/<database-name> --flask --models_layer --controller_layer --outdir ddist[--tables <tablenames>] [--notables] 
```

How To use:
```sh
sqlalchemy-codegen mysql+pymysql://root:password@ip:port/database --flask --models_layer --controller_layer --outdir dist
```

example:
```sh
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --flask --models_layer --controller_layer --outdir dist
```
or:

```sh
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --models_layer --controller_layer --outdir dist
```