#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
#
# This file is part of The OpenBlox Game Engine.
#
#     The OpenBlox Game Engine is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     The OpenBlox Game Engine is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "Apr 20, 2012 11:57:32 AM"


import sys
import urllib2
import threading
import Queue

import obengine.event
import obengine.async


class AsyncUrlOpener(urllib2.HTTPHandler):

    def __init__(self):

        urllib2.HTTPHandler.__init__(self)
        self._response = None
        self._response_lock = threading.Lock()

    def http_response(self, request, response):

        self._response_lock.acquire()
        self._response = response
        self._response_lock.release()

        return response

    def get_response(self):

        self._response_lock.acquire()
        response = self._response
        self._response_lock.release()
        return response


class ExceptionCatchingThread(threading.Thread):

    def __init__(self, *args, **kwargs):

        threading.Thread.__init__(self, *args, **kwargs)
        self.exception_bucket = Queue.Queue()

    def run(self):

        try:
            threading.Thread.run(self)

        except Exception:
            self.exception_bucket.put(sys.exc_info())

class Downloader(object):

    CHUNK_SIZE = 8192
    CONTENT_LENGTH_UNAVAILABLE = -1

    def __init__(self, url, scheduler, raise_exception = False):

        self._url = url
        self._sched = scheduler
        self._raise_exception = raise_exception

        self.on_chunk_recieved = obengine.event.Event()
        self.on_download_complete = obengine.event.Event()

        if self._raise_exception is False:
            self.on_download_failed = obengine.event.Event()

    def start(self):

        self._create_url_opener()
        self._sched.add(obengine.async.Task(self._queue_watcher_task))
        self._thread.start()

    def _validate_thread(self):

        try:

            exc_info = self._thread.exception_bucket.get(block = False)

            exception = exc_info[1]

            if isinstance(exception, urllib2.HTTPError):

                if self._raise_exception is True:
                    raise HTTPException(str(exception))

                else:
                    self.on_download_failed(str(exception))

            else:
                raise exception

        except Queue.Empty:
            pass

    def _create_url_opener(self):

        self._url_hander = AsyncUrlOpener()
        url_opener = urllib2.build_opener(self._url_hander)

        self._thread = ExceptionCatchingThread(target = url_opener.open, args = (self._url,))

    def _queue_watcher_task(self, task):

        self._validate_thread()

        response = self._url_hander.get_response()

        if response is None:
            return task.AGAIN

        self._response = response

        content_length_header = self._response.info().getheader('Content-Length')

        if content_length_header is None:
            self._content_length = Downloader.CONTENT_LENGTH_UNAVAILABLE

        else:
            self._content_length = int(content_length_header)

        self._downloaded_bytes = 0
        self._download_buffer = ''

        self._sched.add(obengine.async.Task(self._data_stream_task))

    def _data_stream_task(self, task):

        self._validate_thread()

        data_chunk = self._response.read(self.CHUNK_SIZE)

        if not data_chunk:

            self.on_download_complete(self._download_buffer)
            return

        data_chunk_length = len(data_chunk)
        self._downloaded_bytes += data_chunk_length
        self._download_buffer += data_chunk

        self.on_chunk_recieved(self._downloaded_bytes, self._content_length)

        return task.AGAIN


class HTTPException(Exception):
    pass
