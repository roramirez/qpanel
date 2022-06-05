# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2022 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from qpanel import backend, config
from redis import Redis
from rq_scheduler import Scheduler
import datetime
import time
from rq import Connection, Worker


DAILY = 1
WEEKLY = 7
MONTHLY = 30
WEEK_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def check_connect_redis():
    try:
        Redis().echo("Check connection")
        return True
    except BaseException:
        return False


def to_utc(dt):
    """ Convert a datetime into datetime as utc time"""
    return datetime.datetime.utcfromtimestamp(dt.timestamp())


def reset_stats_queue(queuename, when, hour):
    '''
        Reset stat for a queue on backend
        queuename: Name of queue to reset
        when, hour parameters for more easy
               control for exists_job_onconfig
    '''
    if not exists_job_onconfig(queuename, when, hour):
        return False
    cfg = config.QPanelConfig()
    b = backend.Backend()
    b.reset_stats(cfg.realname_queue(queuename))
    return True


def job_reset_stats_queue(queuename, when, hour):
    scheduler = Scheduler(connection=Redis())
    remove_jobs_not_config()
    if not exists_job_onqueue(queuename, when, hour):
        at_time = to_utc(datetime_from_config(when, hour))
        scheduler.enqueue_at(at_time, reset_stats_queue, queuename, when, hour)


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


def exists_job_onconfig(queuename, when, hour):
    """ Check if the params for configuration is present for reset_stats"""
    queues_for_reset = config.QPanelConfig().queues_for_reset_stats()
    entry = queues_for_reset.get(queuename)
    if entry and entry['when'] == when and entry['hour'] == hour:
        return True
    return False


def remove_jobs_not_config():
    """
        Remove jobs on queue but not present on config.
        Prevent when in job for reset a queue stats is scheduled but
        after your config is modified or deleted

        TODO: Maybe this could reload by notified in config.ini change
    """
    scheduler = Scheduler(connection=Redis())
    jobs = scheduler.get_jobs()
    for job in jobs:
        if 'reset_stats_queue' in job.func_name:
            # The args for the job of reset_stats_queue are:
            queuename = job.args[0]
            when = job.args[1]
            hour = job.args[2]

            if not exists_job_onconfig(queuename, when, hour):
                job.delete()


def enqueue_reset_stats():
    queues_for_reset = config.QPanelConfig().queues_for_reset_stats()
    for queue, val in queues_for_reset.items():
        job_reset_stats_queue(queue, val['when'], val['hour'])


def get_days_from_val(val):
    val = val.lower()
    day = 0
    if val == 'daily':
        day = DAILY
    elif val in ['weekly'] + WEEK_DAYS:
        day = WEEKLY
    elif val == 'monthly':
        day = MONTHLY
    return day


def give_day_number(value):
    """
    Return a number (weekday) for a string with day configuration.
    By default return 0
    """
    day_number = 0
    if value != 'weekly' and value in WEEK_DAYS:
        day_number = WEEK_DAYS.index(value)
    return day_number


def get_now():
    """ Get the datetime.datetime.now(). Helper to do tests"""
    return datetime.datetime.now()


def datetime_from_config(when, hour):
    """
    Return datetime.datetime for next schedule job by configuration parameters

    This function consider is need it schedule time at today o other day by
    configuration

    :param string when: 'daily', 'monthly', 'weekly' or WEEK_DAYS
    :param string hour: string in %H:%M:%S format

    """
    when = when.lower()  # Fixme
    days = get_days_from_val(when)
    now = get_now()

    st = time.strptime(hour, "%H:%M:%S")
    hour = datetime.time(st.tm_hour, st.tm_min, st.tm_sec)

    # By default at today
    at_time = datetime.datetime(now.year, now.month, now.day,
                                hour.hour, hour.minute, hour.second)

    # Change at_time if match for other conditions
    if days == DAILY:
        if now.time() > hour:
            # scheduler next day
            at_time = at_time + datetime.timedelta(days=1)
    elif days == WEEKLY:
        day_number = give_day_number(when)
        if not (day_number == now.weekday() and now.time() < hour):
            # scheduler next day
            delta = (day_number - now.weekday()) % 7
            if day_number == now.weekday():  # current day for next week
                delta = 7
            at_time = at_time + datetime.timedelta(delta)
    elif days == MONTHLY:
        if not (now.day == 1 and now.time() < hour):
            # scheduler next month
            at_time = last_day_of_month(at_time) + datetime.timedelta(days=1)
    return at_time


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - \
        datetime.timedelta(days=1)


def start_jobs():
    """
        Check if processs enqueue_reset_stats is working on queue if not
        enqueue function
    """
    start_enqueue_reset_stats = True
    scheduler = Scheduler(connection=Redis())
    jobs = scheduler.get_jobs()
    for job in jobs:
        if 'enqueue_reset_stats' in job.func_name:
            start_enqueue_reset_stats = False
            break

    if start_enqueue_reset_stats:
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
