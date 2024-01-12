import sys

from setuptools import setup, find_packages

import codegen

extra_requirements = ()
if sys.version_info < (2, 7):
    extra_requirements = ('argparse',)

setup(
    name='sqlalchemy-codegen',
    description='Automatic generate model layer and controller layer code for SQLAlchemy with Flask support',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version=codegen.version,
    author='iDeal-ncepu',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Database',
        'Topic :: Software Development :: Code Generators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords=['sqlalchemy','flask-sqlalchemy', 'sqlacodegen', 'flask'],
    license='MIT',
    packages=find_packages(exclude=['tests']),
    package_data={'': ['*.json', '*.conf']},
    install_requires=(
        'SQLAlchemy >= 0.6.0',
        'inflect >= 0.2.0',
        'pymysql>= 1.0.2',
        'loguru >= 0.6.0',
        'sqlacodegen>=2.3.0',
        'greenlet>=1.1.2',
    ) + extra_requirements,


    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sqlalchemy-codegen=codegen.main:main'
        ]
    }
)
