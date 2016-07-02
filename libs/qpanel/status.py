import subprocess
import sys
import os
import collections
import utils


def get_mount_partition(types=None):

    partitions = []
    # FIXME: not test
    if 'win' in sys.platform:
        drivelist = subprocess.Popen('wmic logicaldisk get name,description',
                                     shell=True, stdout=subprocess.PIPE)
        drivelisto, err = drivelist.communicate()
        driveLines = drivelisto.split('\n')
    elif 'linux' in sys.platform:
        p = subprocess.Popen("mount", stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        retcode = p.poll()   # returns None while subprocess is running
        lines = p.stdout.readlines()

        for line in lines:
            sline = line.split()
            type = sline[4]
            path_mount = sline[2]

            if types:
                if type in [types]:
                    partitions.append(path_mount)
            else:
                partitions.append(path_mount)
    elif 'macosx':
        # FIXME: not dev
        partitions = []

    return partitions


def disk_usage(path):
    """
    Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
    From :  http://code.activestate.com/recipes/577972-disk-usage/
    """
    _ntuple_diskusage = collections.namedtuple('usage', 'total used free')

    if hasattr(os, 'statvfs'):  # POSIX
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)
    elif os.name == 'nt':       # Windows
        import ctypes

        _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(),\
                ctypes.c_ulonglong()
        if sys.version_info >= (3,) or isinstance(path, unicode):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
        ret = fun(path, ctypes.byref(_), ctypes.byref(total),
                  ctypes.byref(free))

        if ret == 0:
            raise ctypes.WinError()
        used = total.value - free.value
        return _ntuple_diskusage(total.value, used, free.value)
    else:
        raise NotImplementedError("platform not supported")


def get_info_partitions(types=None):
    info = []
    partitions = get_mount_partition(types)
    for partition in partitions:
        usage = disk_usage(partition)

        percent_free = 0
        percent_used = 0
        if usage.total > 0:
            percent_used = usage.used * 100 / usage.total
            percent_free = usage.free * 100 / usage.total

        tmp = {'name': partition,
                'total': {'bytes': usage.total,
                          'bytes2human': utils.bytes2human(usage.total)},
                'used': {'bytes': usage.used,
                         'bytes2human': utils.bytes2human(usage.used),
                         'percent': percent_used},
                'free': {'bytes': usage.free,
                         'bytes2human': utils.bytes2human(usage.free),
                         'percent': percent_free}}

        info.append(tmp)
    return info
