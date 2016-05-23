# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
# Parse queue_log Asterisk file and add records into database.
#

from libs.qpanel import model
import click
import sys

@click.command()
@click.option('--file', default='/var/log/asterisk/queue_log',
              help='Queue Log file.')
@click.option('--verbose', default=False)


def parse(file, verbose):
    inserted, not_inserted = 0, 0
    try:
        with open(file) as fb:
            print("Reading file %s ..." % file)
            content = fb.read().splitlines()
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
                print ("Insert record ",  record)
        else:
            if verbose:
                print ("Not insert record ",  record)
            not_inserted += 1
    print ("Insert record: %i\nNo inserted record: %i" %
        (inserted, not_inserted))


def exist_record(record):
    return model.queuelog_exists_record(record)


def insert_record(record):
    return model.queuelog_insert(record)


if __name__ == '__main__':
    parse()
