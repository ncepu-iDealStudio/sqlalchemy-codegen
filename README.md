## sqlalchemy-codegen

### Introduction

`sqlalchemy-codegen` is an automatic code generation tool based on the SQLAlchemy ORM framework. Through command-line operations, it can automatically generate Model layer and Controller layer code based on existing database structures, significantly improving development efficiency.

### Features

- **Model Layer Generation**: Automatically generate SQLAlchemy Model classes, with each table as a separate Python file
- **Controller Layer Generation**: Automatically generate Controller classes with CRUD operations
- **Flask Framework Support**: Support Flask-SQLAlchemy syntax via `--flask` option
- **Flexible Table Selection**: Support generating code for the entire database or specific tables
- **Relationship Mapping**: Automatically handle foreign key relationships and backrefs between tables
- **Multi-Database Support**: Support MySQL, PostgreSQL and other mainstream databases

### Tech Stack

- Python 3.10+
- SQLAlchemy 2.0+
- sqlacodegen 3.0+
- Flask-SQLAlchemy (optional)

### Project Structure

```
sqlalchemy-codegen/
├── codegen/                          # Core code directory
│   ├── main.py                       # Entry point, command-line argument parsing
│   ├── modelcodegen/                 # Model layer code generation module
│   │   ├── codegen.py                # Model code generation core logic
│   │   ├── dialects/                 # Database dialect support
│   │   │   └── postgresql.py         # PostgreSQL specific handling
│   │   └── template/                 # Model template files
│   │       └── filetemplate.py       # File template definitions
│   ├── controllercodegen/            # Controller layer code generation module
│   │   ├── codegenerator.py          # Controller code generation core logic
│   │   └── template/                 # Controller template files
│   │       ├── filetemplate.py       # File templates (CRUD method templates)
│   │       └── codeblocktemplate.py  # Code block templates
│   └── utils/                        # Utility classes
│       ├── tablesMetadata.py         # Database table metadata retrieval
│       ├── commons.py                # Common utility functions
│       └── response_code.py          # Response code definitions
├── test/                             # Test directory
├── setup.py                          # Installation configuration
├── requirements.txt                  # Dependency list
└── README.md                         # English documentation
```

### Installation

#### Option 1: Install via pip (Recommended)

```bash
pip install sqlalchemy-codegen
```

#### Option 2: Install from source

```bash
git clone https://github.com/ncepu-iDealStudio/sqlalchemy-codegen.git
cd sqlalchemy-codegen/
pip install -e .
```

### Usage

#### Basic Syntax

```bash
sqlalchemy-codegen <database-url> [options]
```


#### Command-Line Options

| Option | Description |
|--------|-------------|
| `--flask` | Use Flask-SQLAlchemy syntax |
| `--models_layer` | Generate Model layer code |
| `--controller_layer` | Generate Controller layer code |
| `--outdir <directory>` | Specify output directory |
| `--tables <table-names>` | Specify tables to generate (comma-separated) |
| `--schema <schema>` | Specify database schema |
| `--noviews` | Ignore views |
| `--noindexes` | Ignore indexes |
| `--noconstraints` | Ignore constraints |
| `--nobackrefs` | Don't generate backrefs |
| `--noinflect` | Don't convert table names to singular form |
| `--noclasses` | Only generate table definitions, not classes |
| `--notables` | Only generate classes, not table definitions |
| `--nocomments` | Don't render column comments |
| `--ignore-cols <columns>` | Ignore specified columns (comma-separated) |
| `--version` | Show version number |

#### Examples

**Example 1: Generate Flask project code**

```bash
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --flask --models_layer --controller_layer --outdir dist
```

**Example 2: Generate plain SQLAlchemy code**

```bash
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --models_layer --controller_layer --outdir dist
```

**Example 3: Generate code for specific tables only**

```bash
sqlalchemy-codegen mysql+pymysql://root:123456@127.0.0.1:3306/testdb --flask --models_layer --tables user,order --outdir dist
```

**Example 4: Connect to PostgreSQL database**

```bash
sqlalchemy-codegen postgresql+psycopg2://user:password@localhost:5432/mydb --flask --models_layer --controller_layer --outdir dist
```

### Generated Code Examples

#### Generated Model File Example

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

#### Generated Controller File Example

```python
# coding: utf-8
import datetime
import math
from ..models import db
from ..models.user import User

class UserController(User):
    
    @classmethod
    def add(cls, **kwargs):
        # Add record
        ...
    
    @classmethod
    def get(cls, **kwargs):
        # Query records (with pagination)
        ...
    
    @classmethod
    def update(cls, **kwargs):
        # Update record
        ...
    
    @classmethod
    def delete(cls, **kwargs):
        # Delete record
        ...
```


### Contributing

We welcome contributions of all kinds, including but not limited to: feature development, bug fixes, documentation improvements, and test case writing.

#### Contribution Workflow

1. **Fork the Repository**

   Visit [GitHub](https://github.com/ncepu-iDealStudio/sqlalchemy-codegen) or [Gitee](https://gitee.com/ncepu-bj/sqlalchemy-codegen), and click the Fork button to copy the project to your account.

2. **Clone to Local**

   ```bash
   git clone https://github.com/<your-username>/sqlalchemy-codegen.git
   cd sqlalchemy-codegen
   ```

3. **Create a Development Branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-you-are-fixing
   ```

4. **Set Up Development Environment**

   ```bash
   # Create virtual environment
   python -m venv env
   
   # Activate virtual environment
   # Windows:
   env\Scripts\activate
   # Linux/Mac:
   source env/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

5. **Develop and Test**

   ```bash
   # Run code generation test (requires a test database)
   python -m codegen.main mysql+pymysql://<username>:<password>@<host>:<port>/<database> --flask --models_layer --controller_layer --outdir dist
   
   # Verify generated code syntax
   python -m py_compile dist/models/__init__.py
   python -m py_compile dist/controller/*.py
   ```

6. **Commit Your Code**

   ```bash
   git add .
   git commit -m "feat: add xxx feature" 
   # or "fix: fix xxx issue"
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

   Create a Pull Request on GitHub/Gitee, describe your changes, and wait for code review.

#### Code Standards

- Follow PEP 8 Python code style guidelines
- Add appropriate comments for new features
- Use clear commit messages, recommended format:
  - `feat: new feature description`
  - `fix: bug fix description`
  - `docs: documentation update description`
  - `refactor: refactoring description`

#### Core Module Description

| Module | Path | Description |
|--------|------|-------------|
| Entry Point | `codegen/main.py` | Command-line argument parsing, coordinating modules |
| Model Generation | `codegen/modelcodegen/codegen.py` | Model layer code generation core logic |
| Controller Generation | `codegen/controllercodegen/codegenerator.py` | Controller layer code generation core logic |
| Model Templates | `codegen/modelcodegen/template/` | Model file template definitions |
| Controller Templates | `codegen/controllercodegen/template/` | Controller file and code block templates |
| Utilities | `codegen/utils/` | Table metadata retrieval, common functions, etc. |

#### Issue Reporting

If you find a bug or have a feature suggestion, please report it through:

- [GitHub Issues](https://github.com/ncepu-iDealStudio/sqlalchemy-codegen/issues)
- [Gitee Issues](https://gitee.com/ncepu-bj/sqlalchemy-codegen/issues)

### Links

- GitHub: https://github.com/ncepu-iDealStudio/sqlalchemy-codegen
- Gitee: https://gitee.com/ncepu-bj/sqlalchemy-codegen
- PyPI: https://pypi.org/project/sqlalchemy-codegen/
- Documentation: https://idealstudio-ncepu.yuque.com/docs/share/b5dcc5ff-fcba-4efd-8955-faeba859bfcf

### Acknowledgments

This project is based on [sqlacodegen](https://github.com/agronholm/sqlacodegen) for secondary development. Thanks to [Alex Grönholm](https://github.com/agronholm) and all contributors for their excellent work.

`sqlacodegen` is a tool that can read existing database structures and generate SQLAlchemy model code. We have made the following extensions based on it:

- Added Controller layer code generation functionality
- Support for separating each table's Model into independent files
- Enhanced Flask-SQLAlchemy integration support
- Optimized relationship mapping and backref handling

### License

MIT License
