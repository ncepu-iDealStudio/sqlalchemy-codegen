from setuptools import setup, find_packages

import codegen

setup(
    name='sqlalchemy-codegen',
    description='Automatic generate model layer and controller layer code for SQLAlchemy with Flask support',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    version=codegen.version,
    author='iDeal-ncepu',
    author_email='idealstudio@ncepu.edu.cn',
    url='https://github.com/ncepu-iDealStudio/sqlalchemy-codegen',
    project_urls={
        'Documentation': 'https://idealstudio-ncepu.yuque.com/docs/share/b5dcc5ff-fcba-4efd-8955-faeba859bfcf',
        'Source': 'https://github.com/ncepu-iDealStudio/sqlalchemy-codegen',
        'Tracker': 'https://github.com/ncepu-iDealStudio/sqlalchemy-codegen/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Database',
        'Topic :: Software Development :: Code Generators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    keywords=['sqlalchemy', 'flask-sqlalchemy', 'sqlacodegen', 'flask', 'code-generator', 'orm'],
    license='MIT',
    packages=find_packages(exclude=['tests', 'test']),
    package_data={'': ['*.json', '*.conf']},
    python_requires='>=3.10',
    install_requires=[
        'SQLAlchemy>=2.0.0',
        'inflect>=7.0.0',
        'sqlacodegen>=3.0.0',
    ],
    extras_require={
        'mysql': ['pymysql>=1.0.0'],
        'postgresql': ['psycopg2-binary>=2.9.0'],
        'dev': [
            'pytest>=7.0.0',
            'flask>=3.0.0',
            'flask-sqlalchemy>=3.1.0',
        ],
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sqlalchemy-codegen=codegen.main:main'
        ]
    }
)
