#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  mks925.py
#  Copyright 2017 Kevin Cole <kevin.cole@novawebcoop.org> 2017.11.18
#
#  Nature Abhors a Vacuum Gauge
#  (Horror METIOR vacuo)
#
#  This little ditty logs the pressure read from the [MKS Instruments 925 Micro
#  Pirani(TM) Vacuum Transducer] ten times per second, both to the screen and
#  to a file named vacuum.log.
#
#    * Press [Enter] to begin logging.
#    * Press Ctrl-C  to close the log and exit.
#
#  For specs on the vacuum transducer, see:
#  https://www.mksinst.com/product/Product.aspx?ProductID=648
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
import re
from   time   import sleep, strftime
from   serial import Serial


__appname__    = "seminal"
__author__     = "Kevin Cole"
__copyright__  = "Copyright \N{copyright sign} 2017"
__agency__     = "HacDC"
__credits__    = ["Kevin Cole"]  # Authors and bug reporters
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Kevin Cole"
__email__      = "kjcole@member.fsf.org"
__status__     = "Prototype"  # "Prototype", "Development" or "Production"
__module__     = "mks925"


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S")


class Gauge(Serial):
    """MKS Instruments 925 Micro Pirani(TM) Vacuum Transducer"""

    def __init__(self):
        super(Gauge, self).__init__()

        # Queries
        #
        self.query = {}
        self.query["pressure-3"] = b"@254PR1?;FF"  # Read pressure (3-digit)
        self.query["pressure-4"] = b"@254PR4?;FF"  # Read pressure (4-digit)

        # Responses
        #
        self.ack = {}
        self.ack["pressure"] = re.compile(b"@\d{3}ACK(.*);FF")

        # Error messages
        #
        self.nak = {}
        self.nak["syntax"]   = re.compile(b"@\d{3}NAK160;FF")

    def connect(self, port="/dev/ttyS0", baudrate=9600):
        """Open a communication channel to the MKS925"""
        self.port     = port
        self.baudrate = baudrate
        self.open()

    def disconnect(self):
        """Close a communication channel to the MKS925"""
        self.close()

    def log(self):
        self.log = open("vacuum.log", "w")

        entry = "Logging begun at: {0}\n".format(timestamp())
        sys.stdout.write(entry)
        self.log.write(entry)

        while True:
            try:
                self.channel.write(self.query["pressure-4"])
                response = self.channel.read(100)
                found = self.ack["pressure"].match(response)
                if found:
                    torr  = float(found.groups()[0])
                    entry = "{0} {1}\n".format(timestamp(), torr)
                    sys.stdout.write(entry)
                    self.log.write(entry)
                sleep(0.1)
            except KeyboardInterrupt:
                entry = "Logging finished at: {0}\n".format(timestamp())
                sys.stdout.write(entry)
                self.log.write(entry)
                self.log.close()
                sys.exit()

    def quit(self):
        self.disconnect()
        sys.exit()
