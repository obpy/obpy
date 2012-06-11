import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine.async
import obengine.net.http


downloaded = False


def progress_func(bytes_so_far, total_size):
    print 'Downloaded', bytes_so_far, 'bytes out of', total_size, 'bytes (%d%%)' % (float(bytes_so_far) / total_size * 100)


def download_complete(data):

    print 'Download complete'
    global downloaded
    downloaded = True


def idle_task(task):

    global downloaded

    if downloaded is False:

        print 'This task is running while a file is being downloaded!'
        return task.AGAIN


scheduler = obengine.async.Scheduler()
downloader = obengine.net.http.Downloader('http://openblox.sourceforge.net/sites/default/files/oblogo-small.png', scheduler)
downloader.on_chunk_recieved += progress_func
downloader.on_download_complete += download_complete

downloader.start()
scheduler.add(obengine.async.PeriodicTask(idle_task, 1.0))
scheduler.loop()
