#!/bin/sh
#
# Copyright 2019 Mathijs Lagerberg.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.
#
#
### BEGIN INIT INFO
# Provides:		epdash
# Required-Start:	$local_fs $remote_fs $syslog
# Required-Stop:	$local_fs $remote_fs $syslog
# Should-Start:		$network
# Should-Stop:		$network
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description: 	Runs E-paper Dashboard
# Description:			Runs E-paper Dashboard
### END INIT INFO

start() {
	echo "Starting E-paper service..."
	sudo python /home/pi/epaperdash/src/main.py &
}

stop() {
	echo "Stopping E-paper service..."
	# TODO this sucks
	sudo killall python
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart|reload|force-reload)
		stop
		sleep 5s
		start
		;;
	status)
		;;
	*)
		echo "Usage: ?"
		exit 1
		;;
esac

exit 0
