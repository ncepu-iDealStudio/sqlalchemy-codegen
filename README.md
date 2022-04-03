# Flask-RESTfulCodegen

Fork of [flask-sqlacodegen](https://github.com/ksindi/flask-sqlacodegen) by Kamil Sindi. Based off of version 1.1.8.

What's different:
* Support for generate Resource layer,include RESTful API based Flask-RESTful.
* Support for generate Model layer.
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
pip install Flask-RESTfulCodegen
```

Without pip:
```sh
git clone https://gitee.com/ncepu-bj/flask-restful-codegen.git
cd flask-restful-codegen/
python setup.py install
```

For contributing:
```sh
git clone https://gitee.com/ncepu-bj/flask-sqlalchemy-codegen
python -m venv env
pip install -r requirements.txt
python -m sqlacodegen.main mysql+pymysql://<username>:<password>@<database-ip>:<port>/<database-name> --flask --models_layer --controller_layer --outdir ddist[--tables <tablenames>] [--notables] 
```