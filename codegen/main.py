#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:main.py
# update by:jackiex
# datetime:2024/1/13 14:56
# software: PyCharm

from __future__ import unicode_literals, division, print_function, absolute_import

import argparse
import importlib
import os
import sys

import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from . import modelcodegen
from .controllercodegen.codegenerator import CodeGenerator as ControllerCodeGenerator
from .modelcodegen.codegen import CodeGenerator as ModelCodeGenerator
from .utils.tablesMetadata import TableMetadata


def import_dialect_specificities(engine):
    dialect_name = '.' + engine.dialect.name
    try:
        importlib.import_module(dialect_name, 'modelcodegen.dialects')
    except ImportError:
        pass


# define generator function for model layer
def generate_model_code(engine, metadata, out_dir, args):
    tables = args.tables.split(',') if args.tables else None
    metadata.reflect(engine, args.schema, not args.noviews, tables)

    ignore_cols = args.ignore_cols.split(',') if args.ignore_cols else None

    model_dir = os.path.join(out_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)

    model_generator = ModelCodeGenerator(metadata, args.noindexes, args.noconstraints,
                                   args.nojoined, args.noinflect, args.nobackrefs,
                                   args.flask, ignore_cols, args.noclasses, args.nocomments, args.notables)

    model_generator.render(model_dir)


# define generator function for controller layer
def generate_controller_code(engine, metadata, out_dir, args):
    metadata.bind = engine

    controller_dir = os.path.join(out_dir, 'controller')
    os.makedirs(controller_dir, exist_ok=True)

    ignore_cols = args.ignore_cols.split(',') if args.ignore_cols else None
    generator = ModelCodeGenerator(metadata, args.noindexes, args.noconstraints,
                                   args.nojoined, args.noinflect, args.nobackrefs,
                                   args.flask, ignore_cols, args.noclasses, args.nocomments, args.notables)
    reflection_views = [model.table.name for model in generator.models if
                        type(model) == modelcodegen.codegen.ModelTable]
    views = sqlalchemy.inspect(engine).get_view_names()

    for table_name in set(reflection_views) ^ set(views):
        print(f"\033[33mWarnning: Table {table_name} required PrimaryKey!\033[0m")
    table_dict = TableMetadata.get_tables_metadata(
        metadata=metadata,
        reflection_views=reflection_views,
    )

    Controller_generator = ControllerCodeGenerator(table_dict, args.flask, args.url)
    Controller_generator.render(controller_dir=controller_dir)


def main():
    parser = argparse.ArgumentParser(description='Generates SQLAlchemy model code from an existing database.')
    parser.add_argument('url', nargs='?', help='SQLAlchemy url to the database')
    parser.add_argument('--version', action='store_true', help="print the version number and exit")
    parser.add_argument('--schema', help='load tables from an alternate schema')
    parser.add_argument('--tables', help='tables to process (comma-separated, default: all)')
    parser.add_argument('--noviews', action='store_true', help="ignore views")
    parser.add_argument('--noindexes', action='store_true', help='ignore indexes')
    parser.add_argument('--noconstraints', action='store_true', help='ignore constraints')
    parser.add_argument('--nojoined', action='store_true', help="don't autodetect joined table inheritance")
    parser.add_argument('--noinflect', action='store_true', help="don't try to convert tables names to singular form")
    parser.add_argument('--noclasses', action='store_true', help="don't generate classes, only tables")
    parser.add_argument('--notables', action='store_true', help="don't generate tables, only classes")
    parser.add_argument('--outdir', help='file to write output to (default: stdout)')
    parser.add_argument('--models_layer', action='store_true', help='model file to write output to direction models')
    parser.add_argument('--controller_layer', action='store_true',
                        help='controller file to write output to direction controllers')
    parser.add_argument('--nobackrefs', action='store_true', help="don't include backrefs")
    parser.add_argument('--flask', action='store_true', help="use Flask-SQLAlchemy columns")
    parser.add_argument('--ignore-cols',
                        help="Don't check foreign key constraints on specified columns (comma-separated)")
    parser.add_argument('--nocomments', action='store_true', help="don't render column comments")
    args = parser.parse_args()

    if args.version:
        print(modelcodegen.version)
        return
    if not args.url:
        print('You must supply a url\n', file=sys.stderr)
        parser.print_help()
        return

    # default_schema = args.default_schema
    # if not default_schema:
    #     default_schema = None

    engine = create_engine(args.url)
    import_dialect_specificities(engine)
    metadata = MetaData()

    # 如果要生成 model 或 controller 层代码，必须指定输出目录
    if args.models_layer or args.controller_layer:
        if not args.outdir:
            outdir = input('Please enter the output directory (e.g., dist): ').strip()
            if not outdir:
                print('Output directory is required. Exiting.\n', file=sys.stderr)
                return
        else:
            outdir = args.outdir
    else:
        outdir = args.outdir if args.outdir else '.'

    # 如果参数中要求生成model层代码
    if args.models_layer:
        generate_model_code(engine, metadata, outdir, args)

    # 如果参数中要求生成控制器层的代码
    if args.controller_layer:
        generate_controller_code(engine, metadata, outdir, args)


if __name__ == '__main__':
    main()
