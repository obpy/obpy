#!/usr/bin/env python

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import sys
import os
import platform
import ConfigParser
import cStringIO
import zipfile

sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.abspath(os.pardir))

import obengine.async
import obengine.net.http


SERVER_INFO_FILE = 'update_info.ini'
UPDATE_SERVER = 'http://openblox.sourceforge.net'
UPDATE_URL = '/'.join((UPDATE_SERVER, SERVER_INFO_FILE))


def get_proper_download_archive(version, config_parser):

    host_os = platform.system().lower()
    return config_parser.get(version, host_os)


def get_available_versions(config_parser):
    return config_parser.get('info', 'versions').strip().split()


def get_supported_oses(config_parser):
    return config_parser.getb('info', 'oses').strip().split()


def start_info_file_download(scheduler):

    downloader = obengine.net.http.Downloader(UPDATE_URL, scheduler)
    downloader.start()

    return downloader


def get_latest_version(config_parser):
    return sorted(get_available_versions(config_parser), key = obengine.compare_versions)[0]


def continue_on_enter():

    print 'Press Enter to continue'
    raw_input()


def download_update(bytes_so_far, total_bytes):

    percentage_downloaded = float(bytes_so_far) / total_bytes * 100
    sys.stdout.write(('%d%%' % percentage_downloaded) % ('\b' * (len(str(percentage_downloaded)) + 1)))


def find_latest_version(update_data, scheduler):

    print '\nDownload complete'

    update_file = cStringIO.StringIO(update_data)
    config_parser = ConfigParser.ConfigParser()
    config_parser.readfp(update_file)

    latest_version = get_latest_version(config_parser)
    if obengine.compare_versions(obengine.version_string(), latest_version) >= 0:

        print 'No new updates'
        continue_on_enter()
        sys.exit(0)

    download_archive = get_proper_download_archive(latest_version, config_parser)
    if download_archive is None:

        print 'Your OS is not supported by this update server'
        continue_on_enter()
        sys.exit(1)

    print 'Downloading update package from', download_archive,
    download_update_archive(download_archive, scheduler)


def download_update_archive(download_archive, scheduler):

    update_downloader = obengine.net.http.Downloader(download_archive, scheduler)
    update_downloader.on_chunk_recieved += download_update
    update_downloader.on_download_complete += install_update_archive

    update_downloader.start()


def get_root_openblox_dir():

    if hasattr(sys, 'frozen') and sys.frozen == 1:

        path = sys.executable
        return path

    else:

        print 'Auto-update functionality is currently only supported for binary builds of OpenBlox'
        continue_on_enter()
        sys.exit(1)


def install_update_archive(update_string):

    print 'Installing update archive'

    update_data = cStringIO.StringIO(update_string)
    update_archive = zipfile.ZipFile(update_data)
    extract_path = get_root_openblox_dir()

    update_archive.extractall(extract_path)

    print 'OpenBlox successfully updated!'
    continue_on_enter()


def main():

    scheduler = obengine.async.Scheduler()

    print 'Downloading update info from', UPDATE_URL,

    downloader = start_info_file_download(scheduler)
    downloader.on_chunk_recieved += download_update
    downloader.on_download_complete += lambda u: find_latest_version(u, scheduler)

    scheduler.loop()


if __name__ == '__main__':
    main()
