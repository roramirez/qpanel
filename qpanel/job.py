# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from qpanel import backend, config
from redis import Redis
from rq_scheduler import Scheduler
import datetime
import time
from rq import Connection, Worker

def check_connect_redis():
    try:
        Redis().echo("Check connection")
        return True
    except:
        return False

def reset_stats_queue(queuename, when, hour):
    '''
        Reset stat for a queue on backend
        queuename: Name of queue to reset
        when, hour parameters for more easy
               control for exists_job_onqueue
    '''
    remove_jobs_not_config()
    if not exists_job_onqueue(queuename, when, hour):
        return False
    b = backend.Backend()
    b.reset_stats(queuename)
    return True


def job_reset_stats_queue(queuename, when, hour):
    scheduler = Scheduler(connection=Redis())
    remove_jobs_not_config()
    if not exists_job_onqueue(queuename, when, hour):
        scheduler.schedule(
            scheduled_time=datetime_from_config(when, hour),
            func=reset_stats_queue,
            args=[queuename, when, hour],
            interval=seconds_from_config_interval(when)
        )


def exists_job_onqueue(queuename, when, hour):
    """
        Check if a job is present on queue
    """
    scheduler = Scheduler(connection=Redis())
    jobs = scheduler.get_jobs()
    for job in jobs:
        if 'reset_stats_queue' in job.func_name:
            args = job.args
            if queuename == args[0] and when == args[1] and hour == args[2]:
                return True
    return False


def remove_jobs_not_config():
    """
        Remove jobs on queue but not present on config.
        Prevent when in job for reset a queue stats is scheduled but
        after your config is modified or deleted
    """
    scheduler = Scheduler(connection=Redis())
    queue_for_reset = config.QPanelConfig().queues_for_reset_stats()
    jobs = scheduler.get_jobs()
    for job in jobs:
        if 'reset_stats_queue' in job.func_name:
            q = job.args[0]
            delete = True
            for qr in queue_for_reset:
                if qr in queue_for_reset:
                    if (queue_for_reset[qr]['when'] == job.args[1] and
                        queue_for_reset[qr]['hour'] == job.args[2]):
                        delete = False
                if delete:
                    job.delete()


def enqueue_reset_stats():
    queues_for_reset = config.QPanelConfig().queues_for_reset_stats()
    for queue, val in queues_for_reset.items():
        job_reset_stats_queue(queue, val['when'], val['hour'])


def get_days_from_val(val):
    val = val.lower()
    day = 0
    if val == 'daily':
        day = 1
    elif val in ['weekly', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']:
        day = 7
    elif val == 'monthly':
        day = 30
    return day


def seconds_from_config_interval(val):
    """
        Get interval value for a configuration by parameter
    """
    # day * hour * minute * seconds
    return get_days_from_val(val) * 24 * 60 * 60


def datetime_from_config(when, hour):
    when = when.lower()  # Fixme
    days = get_days_from_val(when)
    now = datetime.datetime.now()
    ldays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    st = time.strptime(hour, "%H:%M:%S")
    hour = datetime.time(st.tm_hour, st.tm_min, st.tm_sec)

    at_time = datetime.datetime(now.year, now.month, now.day,
                                hour.hour, hour.minute, hour.second)
    if days == 1:
        if now.time() > hour:
            # scheduler next day
            at_time = at_time + datetime.timedelta(days=1)
    elif days == 7:
        if ((now.weekday() == 0 or (now.weekday() == ldays.index(when) + 1))
            and now.time() < hour):
            # scheduler today
            at_time = at_time
        else:
            # scheduler next week
            next_day = 0
            if when is not 'weekly':
                next_day = ldays.index(when)
            at_time = at_time + datetime.timedelta((next_day - now.weekday()) % 7)
    elif days == 30:
        if now.day == 1 and now.time() < hour:
            at_time = at_time
        else:
            # scheduler next month
            at_time = last_day_of_month(at_time) + datetime.timedelta(days=1)
    return at_time


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)


def start_jobs():
    """
        Check if processs enqueue_reset_stats is working on queue if not
        enqueue function
    """
    start_enqueue_reset_stats = False
    scheduler = Scheduler(connection=Redis())
    jobs = scheduler.get_jobs()
    for job in jobs:
        if 'enqueue_reset_stats' in job.func_name:
            start_enqueue_reset_stats = True
            break

    if start_enqueue_reset_stats is False:
        scheduler.schedule(
            scheduled_time=datetime.datetime.utcnow(),
            func=enqueue_reset_stats,
            interval=60
        )


def start_process():
    start_jobs()
    start_workers()


def start_workers(qs=['default']):
    with Connection():
        w = Worker(qs)
        w.work()
