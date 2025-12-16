## sqlalchemy-codegen

### 项目简介

`sqlalchemy-codegen` 是一个基于 SQLAlchemy ORM 框架的代码自动生成工具。通过命令行操作，可以根据现有数据库结构自动生成实体层（Model）和控制器层（Controller）代码，大幅提升开发效率。

### 功能特性

- **实体层代码生成**：自动生成 SQLAlchemy Model 类，每个表对应独立的 Python 文件
- **控制器层代码生成**：自动生成包含 CRUD 操作的 Controller 类
- **Flask 框架支持**：通过 `--flask` 选项支持 Flask-SQLAlchemy 语法
- **灵活的表选择**：支持生成整个数据库或指定表的代码
- **关系映射**：自动处理表之间的外键关系和反向引用（backrefs）
- **多数据库支持**：支持 MySQL、PostgreSQL 等主流数据库

### 技术栈

- Python 3.12+
- SQLAlchemy 2.0.25
- sqlacodegen 3.0.0rc3
- Flask-SQLAlchemy（可选）

<<<<<<< HEAD
项目特性以及所做的改进工作:
* 已经全面支持pyhton3.12,以及重要依赖包的最新版本：sqlacodegen3.0.0rc3，SQLAlchemy2.0.25等.
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


```
sqlalchemy-codegen/
├── codegen/                          # 核心代码目录
│   ├── main.py                       # 程序入口，命令行参数解析
│   ├── modelcodegen/                 # 实体层代码生成模块
│   │   ├── codegen.py                # Model 代码生成核心逻辑
│   │   ├── dialects/                 # 数据库方言支持
│   │   │   └── postgresql.py         # PostgreSQL 特定处理
│   │   └── template/                 # Model 模板文件
│   │       └── filetemplate.py       # 文件模板定义
│   ├── controllercodegen/            # 控制器层代码生成模块
│   │   ├── codegenerator.py          # Controller 代码生成核心逻辑
│   │   └── template/                 # Controller 模板文件
│   │       ├── filetemplate.py       # 文件模板（CRUD 方法模板）
│   │       └── codeblocktemplate.py  # 代码块模板
│   └── utils/                        # 工具类
│       ├── tablesMetadata.py         # 数据库表元数据获取
│       ├── commons.py                # 通用工具函数
│       └── response_code.py          # 响应码定义
├── test/                             # 测试目录
├── setup.py                          # 安装配置
├── requirements.txt                  # 依赖列表
└── README.md                         # 英文文档
```

### 安装方式

#### 方式一：通过 pip 安装（推荐）

```bash
pip install sqlalchemy-codegen
```

#### 方式二：从源码安装

```bash
git clone https://gitee.com/ncepu-bj/sqlalchemy-codegen.git
cd sqlalchemy-codegen/
python setup.py install
或者：
pip install -e .
```

### 使用方法

#### 基本语法

```bash
sqlalchemy-codegen <数据库连接URL> [选项]
```

#### 命令行选项

| 选项 | 说明 |
|------|------|
| `--flask` | 使用 Flask-SQLAlchemy 语法 |
| `--models_layer` | 生成实体层代码 |
| `--controller_layer` | 生成控制器层代码 |
| `--outdir <目录>` | 指定输出目录 |
| `--tables <表名>` | 指定要生成的表（逗号分隔） |
| `--schema <模式>` | 指定数据库模式 |
| `--noviews` | 忽略视图 |
| `--noindexes` | 忽略索引 |
| `--noconstraints` | 忽略约束 |
| `--nobackrefs` | 不生成反向引用 |
| `--noinflect` | 不转换表名为单数形式 |
| `--noclasses` | 只生成表定义，不生成类 |
| `--notables` | 只生成类，不生成表定义 |
| `--nocomments` | 不渲染字段注释 |
| `--ignore-cols <列名>` | 忽略指定列（逗号分隔） |
| `--version` | 显示版本号 |

#### 使用示例

**示例 1：生成 Flask 项目代码**

```bash
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --flask --models_layer --controller_layer --outdir dist
```

**示例 2：生成普通 SQLAlchemy 代码**

```bash
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --models_layer --controller_layer --outdir dist
```

**示例 3：只生成指定表的代码**

```bash
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --flask --models_layer --tables user,order --outdir dist
```

**示例 4：连接 PostgreSQL 数据库**

```bash
sqlalchemy-codegen postgresql+psycopg2://user:password@localhost:5432/mydb --flask --models_layer --controller_layer --outdir dist
```

### 生成代码示例

#### 生成的 Model 文件示例

```python
# coding: utf-8
from . import db, BaseModel

class User(BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
```

#### 生成的 Controller 文件示例

```python
# coding: utf-8
import datetime
import math
from ..models import db
from ..models.user import User

class UserController(User):
    
    @classmethod
    def add(cls, **kwargs):
        # 添加记录
        ...
    
    @classmethod
    def get(cls, **kwargs):
        # 查询记录（支持分页）
        ...
    
    @classmethod
    def update(cls, **kwargs):
        # 更新记录
        ...
    
    @classmethod
    def delete(cls, **kwargs):
        # 删除记录
        ...
```

### 参与开源贡献

我们欢迎任何形式的贡献，包括但不限于：功能开发、Bug 修复、文档完善、测试用例编写等。

#### 贡献流程

1. **Fork 仓库**

   访问 [GitHub](https://github.com/ncepu-iDealStudio/sqlalchemy-codegen) 或 [Gitee](https://gitee.com/ncepu-bj/sqlalchemy-codegen)，点击 Fork 按钮将项目复制到你的账户下。

2. **克隆到本地**

   ```bash
   git clone https://github.com/<你的用户名>/sqlalchemy-codegen.git
   cd sqlalchemy-codegen
   ```

3. **创建开发分支**

   ```bash
   git checkout -b feature/你的功能名称
   # 或
   git checkout -b fix/你要修复的问题
   ```

4. **搭建开发环境**

   ```bash
   # 创建虚拟环境
   python -m venv env
   
   # 激活虚拟环境
   # Windows:
   env\Scripts\activate
   # Linux/Mac:
   source env/bin/activate
   
   # 安装依赖
   pip install -r requirements.txt
   ```

5. **开发与测试**

   ```bash
   # 运行代码生成测试（需要准备测试数据库）
   python -m codegen.main mysql+pymysql://<username>:<password>@<host>:<port>/<database> --flask --models_layer --controller_layer --outdir dist
   
   # 验证生成的代码语法
   python -m py_compile dist/models/__init__.py
   python -m py_compile dist/controller/*.py
   ```

6. **提交代码**

   ```bash
   git add .
   git commit -m "feat: 添加xxx功能" 
   # 或 "fix: 修复xxx问题"
   git push origin feature/你的功能名称
   ```

7. **创建 Pull Request**

   在 GitHub/Gitee 上创建 Pull Request，描述你的修改内容，等待代码审核。

#### 代码规范

- 遵循 PEP 8 Python 代码风格规范
- 新功能需要添加相应的注释说明
- 提交信息请使用清晰的描述，推荐格式：
  - `feat: 新功能描述`
  - `fix: 修复问题描述`
  - `docs: 文档更新描述`
  - `refactor: 重构描述`

#### 项目核心模块说明

| 模块 | 路径 | 说明 |
|------|------|------|
| 程序入口 | `codegen/main.py` | 命令行参数解析，协调各模块工作 |
| Model 生成 | `codegen/modelcodegen/codegen.py` | 实体层代码生成核心逻辑 |
| Controller 生成 | `codegen/controllercodegen/codegenerator.py` | 控制器层代码生成核心逻辑 |
| Model 模板 | `codegen/modelcodegen/template/` | Model 文件模板定义 |
| Controller 模板 | `codegen/controllercodegen/template/` | Controller 文件和代码块模板 |
| 工具类 | `codegen/utils/` | 表元数据获取、通用函数等 |

#### 问题反馈

如果你发现 Bug 或有功能建议，欢迎通过以下方式反馈：

- [GitHub Issues](https://github.com/ncepu-iDealStudio/sqlalchemy-codegen/issues)
- [Gitee Issues](https://gitee.com/ncepu-bj/sqlalchemy-codegen/issues)

### 相关链接

- GitHub: https://github.com/ncepu-iDealStudio/sqlalchemy-codegen
- Gitee: https://gitee.com/ncepu-bj/sqlalchemy-codegen
- PyPI: https://pypi.org/project/sqlalchemy-codegen/
- 文档: https://idealstudio-ncepu.yuque.com/docs/share/b5dcc5ff-fcba-4efd-8955-faeba859bfcf

### 致谢

本项目基于 [sqlacodegen](https://github.com/agronholm/sqlacodegen) 进行二次开发，感谢 [Alex Grönholm](https://github.com/agronholm) 及所有贡献者的优秀工作。

`sqlacodegen` 是一个能够读取现有数据库结构并生成 SQLAlchemy 模型代码的工具。我们在此基础上进行了以下扩展：

- 新增控制器层（Controller）代码生成功能
- 支持将每个表的 Model 分离为独立文件
- 增强 Flask-SQLAlchemy 集成支持
- 优化关系映射和反向引用处理

### 许可证

MIT License
