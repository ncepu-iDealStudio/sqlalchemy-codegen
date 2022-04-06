""" """
from __future__ import unicode_literals, division, print_function, absolute_import

import argparse
import importlib
import os
import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from . import modelcodegen
from .controllercodegen.codegenerator import CodeGenerator as ControllerCodeGenerator
from .modelcodegen.codegen import CodeGenerator as SQLCodeGenerator
from .utils import commons
from .utils.tablesMetadata import TableMetadata


def import_dialect_specificities(engine):
    dialect_name = '.' + engine.dialect.name
    try:
        importlib.import_module(dialect_name, 'modelcodegen.dialects')
    except ImportError:
        pass

workPath = commons.cur_file_dir()
workPath = os.path.join(workPath, "../Lib/site-packages/codegen")

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
    engine = create_engine(args.url)
    import_dialect_specificities(engine)
    metadata = MetaData(engine)
    tables = args.tables.split(',') if args.tables else None
    ignore_cols = args.ignore_cols.split(',') if args.ignore_cols else None
    metadata.reflect(engine, args.schema, not args.noviews, tables)
    outdir = args.outdir if args.outdir else sys.stdout
    generator = SQLCodeGenerator(metadata, args.noindexes, args.noconstraints,
                                 args.nojoined, args.noinflect, args.nobackrefs,
                                 args.flask, ignore_cols, args.noclasses, args.nocomments, args.notables)

    if args.models_layer:
        os.makedirs(model_dir := os.path.join(outdir, 'models'), exist_ok=True)
        generator.render(model_dir)

    if args.controller_layer:
        os.makedirs(controller_dir := os.path.join(outdir, 'controller'), exist_ok=True)
        reflection_views = [model.table.name for model in generator.models if type(model) == modelcodegen.codegen.ModelTable]
        table_dict = TableMetadata.get_tables_metadata(
            metadata=metadata,
            reflection_views=reflection_views,
        )
        generator = ControllerCodeGenerator(table_dict)
        generator.controller_codegen(controller_dir=controller_dir)
        util_path = os.path.join(outdir, "utils")
        if not os.path.exists(util_path):
            os.mkdir(util_path)
        generator.static_generate(util_path, os.path.join(workPath, "staticTemplate/utils"))


if __name__ == '__main__':
    main()
