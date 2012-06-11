import obengine.async
import obengine.net.http


def progress_func(bytes_so_far, total_size):
   print 'Downloaded', bytes_so_far, 'bytes out of', total_size, 'bytes'


def download_complete(data):
   print 'Download complete'


scheduler = obengine.async.Scheduler()
downloader = obengine.net.http.Downloader('http://openblox.sourceforge.net/sites/default/files/oblogo-small.png', scheduler)
downloader.on_chunk_recieved += progress_func
downloader.on_download_complete += download_complete

downloader.start()
scheduler.loop()
