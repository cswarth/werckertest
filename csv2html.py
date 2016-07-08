#!/usr/bin/env python

import sys
import csv
import pandas as pd
import argparse
import jinja2
import getpass
from jinja2 import Environment, FileSystemLoader
import datetime
import os

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def render(table, fp, templatefile):
    env = Environment(loader=FileSystemLoader(THIS_DIR),
                          trim_blocks=True)
    # Alias str.format to strformat in template
    env.filters['strformat'] = str.format
    template = env.get_template(templatefile)
    template.stream(table=table,
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user=getpass.getuser(),
            command=" ".join(sys.argv),
            workdir=os.getcwd()).dump(fp)

    
def main():
    p = argparse.ArgumentParser()
    p.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    p.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    p.add_argument('-t', '--template', default='template.jinja',
            help="""Jinja2 Tempate file[default: %(default)]""")
    a = p.parse_args()
    
    df = pd.read_csv(a.infile)
    tbl = df.to_html(index=False, index_names=False, classes="table table-bordered table-striped table-condensed")

    with a.outfile as fp:
        render(tbl, fp, a.template)


if __name__ == '__main__':
    main()
