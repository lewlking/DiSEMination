#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  monitor.py
#  Copyright 2017 Kevin Cole <kevin.cole@novawebcoop.org> 2017.11.17
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
import serial
import re
from   time   import sleep, strftime


__appname__    = "Horror METIOR vacuo"
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


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S")


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

    input("Nature abhors a vacuum gauge. Press [Enter] to start, Ctrl-C to end.")

    mks925 = serial.Serial("/dev/ttyS0", 9600, timeout=0, rtscts=False)

    query = {}
    query["pressure-3"] = b"@254PR1?;FF"  # Return pressure as a 3-digit value
    query["pressure-4"] = b"@254PR4?;FF"  # Return pressure as a 4-digit value

    ack = {}
    ack["pressure"] = re.compile(b"@\d{3}ACK(.*);FF")

    nak = {}
    nak["syntax"]   = re.compile(b"@\d{3}NAK160;FF")

    log = open("vacuum.log", "w")

    entry = "Logging begun at: {0}\n".format(timestamp())
    sys.stdout.write(entry)
    log.write(entry)

    tenths = 0

    while True:
        try:
            mks925.write(query["pressure-4"])
            response = mks925.read(100)
            found = ack["pressure"].match(response)
            if found:
                torr      = float(found.groups()[0])
                entry = "{0:6}\t{1}\n".format(tenths, torr)
                sys.stdout.write(entry)
                log.write(entry)
                tenths += 1
            sleep(0.1)
        except KeyboardInterrupt:
            entry = "Logging finished at: {0}\n".format(timestamp())
            sys.stdout.write(entry)
            log.write(entry)
            log.close()
            sys.exit()
    return 0


if __name__ == "__main__":
    main()
