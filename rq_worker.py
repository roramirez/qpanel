from libs.qpanel.job import start_process
from multiprocessing import Process

def start_jobs():
    p = Process(target=start_process)
    p.start()

if __name__ == '__main__':
    start_jobs()
