#!/usr/bin/python
# -*- coding: utf-8 -*-

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


from datetime import datetime
import logging
import time
import sys
import traceback

from howcold.HowColdView import HowColdView
from howcold.HowColdController import HowColdController
from weather.WeatherView import WeatherView
from weather.WeatherController import WeatherController
from status.StatusView import StatusView
from status.StatusController import StatusController
from clock.ClockView import ClockView
from clock.ClockController import ClockController


def init_logger():
    logger = logging.getLogger('../logs/epd-service')
    hdlr = logging.FileHandler('../logs/epd-service.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


def main(argv):

    # init controllers and views
    weather = WeatherController(logger, WeatherView())
    status = StatusController(StatusView())
    clock = ClockController(ClockView())

    while True:
        # update controllers
        weather_updated = weather.update()
        status_updated = status.update()
        clock_updated = clock.update()
        
        # check if we need to exit
        stop = weather.requests_exit() or \
            status.requests_exit() or \
            clock.requests_exit()
        if stop:
            break

        # render views
        draw = None
        if weather_updated:
            weather.get_view().render(draw)
        if status_updated:
            status.get_view().render(draw)
        if clock_updated:
            clock.get_view().render(draw)

        # pause one second
        time.sleep(1)
    
    # finish controllers
    weather.finish()
    status.finish()
    clock.finish()


#main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    logger = init_logger()
    exit_status = None
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        print("Fetching weather...")
        WeatherController(logger, WeatherView()).fetch_weather()
        print("Done")
    else:
        try:
            # do the thing
            main(sys.argv[1:])
        except KeyboardInterrupt:
            logger.info('keyboard interrupt')
            exit_status = 'interrupted'
        except Exception as e:
            traceback.print_exc()
            logger.exception(e)
            exit_status = 'exception'
    if not exit_status is None:
        sys.exit(exit_status)
        
