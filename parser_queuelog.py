# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
# Parse queue_log Asterisk file and add records into database.
#

import sys
import tailer
from qpanel import model
import click


@click.command()
@click.option('--file', default='/var/log/asterisk/queue_log',
              help='Queue Log file.')
@click.option('--lines', default=None, help='Get the last lines from file.')
@click.option('--verbose', default=False)
def parse(file, verbose, lines):
    inserted, not_inserted = 0, 0
    try:
        if lines is None:
            fb = open(file)
            content = fb.read().splitlines()
        else:
            nlines = int(lines)
            content = tailer.tail(open(file), nlines)
        print('Reading file %s ...' % file)

    except IOError:
        print('File file %s not exits or not can read.' % file)
        sys.exit(1)

    for idx, line in enumerate(content):
        record = line.split('|')
        if len(record) < 4:
            continue
        if not exist_record(record) and insert_record(record):
            inserted += 1
            if verbose:
                print(('Insert record ', record))
        else:
            if verbose:
                print(('Not insert record ', record))
            not_inserted += 1
    print('Insert record: %i\nNo inserted record: %i' % (inserted,
                                                         not_inserted))


def exist_record(record):
    return model.queuelog_exists_record(record)


def insert_record(record):
    return model.queuelog_insert(record)


if __name__ == '__main__':
    parse()
