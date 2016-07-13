import backend
import config
from redis import Redis
from rq_scheduler import Scheduler
import datetime
from rq import Connection, Worker


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
            if q not in queue_for_reset.keys():
                job.delete()


def enqueue_reset_stats():
    queues_for_reset = config.QPanelConfig().queues_for_reset_stats()
    for queue, val in queues_for_reset.items():
        job_reset_stats_queue(queue, val['when'], val['hour'])


def seconds_from_config_interval(val):
    """
        Get interval value for a configuration by parameter
    """
    val = val.lower()
    day = 0
    if val == 'daily':
        day = 1
    elif val in ['weekly', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri' 'sat']:
        day = 7
    elif val == 'monthly':
        day = 30
    return day * 24 * 60 * 60  # day *  hour * minute * seconds


def datetime_from_config(when, hour):
    return datetime.datetime.utcnow()


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
