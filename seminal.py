#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  seminal.py
#  Copyright 2017 Kevin Cole <kevin.cole@novawebcoop.org> 2017.11.18
#
#  Scanning Electron Microscope interface
#
#    * Press [Enter] to begin logging.
#    * Press Ctrl-C  to close the log and exit.
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with this program; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.
#


import os
import sys
from   mks925 import Gauge

__appname__    = "SEMinal"
__author__     = "Kevin Cole"
__copyright__  = "Copyright \N{copyright sign} 2017"
__agency__     = "HacDC"
__credits__    = ["Kevin Cole"]  # Authors and bug reporters
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Kevin Cole"
__email__      = "kjcole@member.fsf.org"
__status__     = "Prototype"  # "Prototype", "Development" or "Production"
__module__     = ""


def main():
    _ = os.system("clear")
    print("{0} v.{1}\n{2} ({3})\n{4}, {5} <{6}>\n"
          .format(__appname__,
                  __version__,
                  __copyright__,
                  __license__,
                  __author__,
                  __agency__,
                  __email__))

    gauge = Gauge()
    commands = {"connect":    gauge.connect,
                "disconnect": gauge.disconnect,
                "log":        gauge.log,
                "quit":       gauge.quit}

    while True:
        command = input("> ")
        if command in commands:
            commands[command]

    return 0


if __name__ == "__main__":
    main()
