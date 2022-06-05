# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2022 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from qpanel import config, job, rq_worker


if __name__ == '__main__':
    """
        Simple program to run worker for reset stats of Queue

        If you are running the QPanel using a uwsgi script should use
        this script to run background process will be reset stats for
        the queues

        see samples/resetstats_supervisor.conf
    """

    cfg = config.QPanelConfig()

    if cfg.queues_for_reset_stats():
        if job.check_connect_redis():
            rq_worker.start_jobs()
        else:
            print("Error: There not connection to Redis")
            print("       Reset stats will not work\n")
