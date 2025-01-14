#!/usr/bin/env python3
# Stratosphere Linux IPS. A machine-learning Intrusion Detection System
# Copyright (C) 2021 Sebastian Garcia

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# Contact: eldraco@gmail.com, sebastian.garcia@agents.fel.cvut.cz, stratosphere@aic.fel.cvut.cz

from __future__ import print_function
import sys
import os
import time
import warnings

# Ignore warnings on CPU from tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# Ignore warnings in general
warnings.filterwarnings('ignore')


####################
# Main
####################
if __name__ == '__main__':

    if sys.version_info[0] < 3:
        sys.exit("Slips can only run on python3+ .. Stopping.")

    from slips.main import Main
    from slips.daemon import Daemon

    slips = Main()
    # checker = Checker(slips)
    # checker.check_python_version()

    if slips.args.stopdaemon:
        # -S is provided
        daemon = Daemon(slips)
        if not daemon.pid:
            # pidfile doesn't exist
            print("Trying to stop Slips daemon.\n Daemon is not running.")
        else:
            daemon.stop()
            # it takes about 5 seconds for the stop_slips msg
            # to arrive in the channel, so give slips time to stop
            time.sleep(3)
            print('Daemon stopped.')
    elif slips.args.daemon:
        daemon = Daemon(slips)
        if daemon.pid is not None:
            print('pidfile already exists. Daemon already running?'
                  .format(daemon.pidfile))
        else:
            print('Slips daemon started.')
            daemon.start()
    else:
        # interactive mode
        slips.start()

    slips.cpu_profiler_release()
    slips.memory_profiler_release()
