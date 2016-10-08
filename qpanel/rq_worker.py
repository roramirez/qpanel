from qpanel.job import start_process
from multiprocessing import Process
from rq_scheduler.scripts.rqscheduler import main


def start_jobs():
    p = Process(target=start_process)
    p.start()
    start_scheduler()

def start_scheduler():
    p = Process(target=main)
    p.start()


if __name__ == '__main__':
    start_jobs()
