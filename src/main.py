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
from EPD import EPD
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw

from weather.WeatherEpdView import WeatherEpdView
from weather.WeatherController import WeatherController
from status.StatusEpdView import StatusEpdView
from status.StatusController import StatusController
from clock.ClockEpdView import ClockEpdView
from clock.ClockController import ClockController
import constants

button_pressed = constants.BUTTON_NONE

def on_click(button):
    global button_pressed
    button_pressed = button
    print('Button pressed: %s'%button_pressed)

def init_logger():
    logger = logging.getLogger('../logs/epd-service')
    hdlr = logging.FileHandler('../logs/epd-service.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def main(argv):
    # use broadcom GPIO designations
    GPIO.setmode(GPIO.BCM)
    # warning messages
    GPIO.setwarnings(True)
    # set button listeners
    for button in constants.BUTTONS:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(button, GPIO.FALLING, callback=on_click, bouncetime=500)
    # clear screen
    epd = EPD()
    print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog, f=epd.film))
    #epd.clear()
    # start main loop
    main_loop(epd)


def main_loop(epd):
    global button_pressed
    
    # initially set all white background
    image = Image.new('1', epd.size, constants.WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size
    # clear the display buffer
    draw.rectangle((0, 0, width, height), fill=constants.WHITE, outline=constants.WHITE)

    # init controllers and views
    weather = WeatherController(logger, WeatherEpdView(epd))
    status = StatusController(StatusEpdView(epd))
    clock = ClockController(ClockEpdView(epd))

    while True:
    
        # handle input
        if button_pressed != constants.BUTTON_NONE:
            if status.on_click(button_pressed):
                button_pressed = constants.BUTTON_NONE
        
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
        must_clear = status_updated and status.get_view().must_update_fully()
        updated = weather_updated or status_updated or clock_updated
        if must_clear:
            status.get_view().clear(draw)
        if clock_updated:
            clock.get_view().render(draw)
        if weather_updated:
            weather.get_view().render(draw)
        if status_updated:
            status.get_view().render(draw)

        # update display
        if updated:
            #image.save("screenshot.png")
            epd.display(image)
            fully = clock.get_view().must_update_fully() or \
                weather.get_view().must_update_fully() or \
                status.get_view().must_update_fully()
            if fully:
                epd.update()
            else:
                epd.partial_update()

        # pause one sec
        time.sleep(1)
    
    # finish controllers
    weather.finish()
    status.finish()
    clock.finish()


# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    logger = init_logger()
    exit_status = None
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        print("Fetching weather...")
        WeatherController().fetch_weather()
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
        finally:
            GPIO.cleanup()
    if not exit_status is None:
        sys.exit(exit_status)
        
