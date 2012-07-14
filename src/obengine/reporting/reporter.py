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
__date__ = "Jul 12, 2012 4:43:29 PM"


import sys


error_reporter = None
info_reporter = None


class ErrorReporter(object):

    def report_error(self, message):
        raise NotImplementedError

    def report_error_blocking(self, message):
        raise NotImplementedError


class InfoReporter(object):

    def report_info(self, message):
        raise NotImplementedError

    def report_info_blocking(self, message):
        raise NotImplementedError


class ConsoleErrorReporter(ErrorReporter):

    def report_error(self, message):
        print >> sys.stderr, message

    def report_error_blocking(self, message):

        self.report_error(message)
        print >> sys.stderr, 'Press Enter to continue'
        raw_input()


class ConsoleInfoReporter(InfoReporter):

    def report_info(self, message, newline = True):

        if newline is True:
            print message

        else:
            sys.stdout.write(message)

    def report_info_blocking(self, message, newline = True):

        self.report_info(message, newline)
        print 'Press Enter to continue'
        raw_input()


def set_error_reporter(reporter):

    global error_reporter
    error_reporter = reporter


def report_error(message):
    error_reporter.report_error(message)


def report_error_blocking(message):
    error_reporter.report_error_blocking(message)


set_error_reporter(ConsoleErrorReporter())


def set_info_reporter(reporter):

    global info_reporter
    info_reporter = reporter


def report_info(message, newline = True):
    info_reporter.report_info(message)


def report_info_blocking(message, newline = True):
    info_reporter.report_info_blocking(message)


set_info_reporter(ConsoleInfoReporter())
