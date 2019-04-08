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


import constants
from View import View
from WeatherView import WeatherView
from PIL import ImageFont
from PIL import Image
import os.path

TEXT_SIZE_TIME = 16
TEXT_SIZE_TEMP = 24
LINE_WIDTH = 3
LEFT = 4
TOP_GRAPH = 60
TOP_TEMPERATURE = 105
TOP_TIME = 133
GRAPH_HEIGHT = TOP_TEMPERATURE - TOP_GRAPH - 4
COLUMN_WIDTH = 32
COLUMN_MARGIN = 12
COLUMNS = 5
ICON_SIZE = 30, 30
ICON_PATH = 'assets/icons/{0}.png'

class WeatherEpdView(WeatherView):
    """
    View that displays a WeatherModel as a graph
    with temperatures and condition icons.
    """

    temp_font = ImageFont.truetype(constants.FONT_FILE, TEXT_SIZE_TEMP)
    title_font= ImageFont.truetype(constants.FONT_FILE, TEXT_SIZE_TIME)

    def __init__(self, epd):
        WeatherView.__init__(self, epd)

    def get_size(self):
        width,height = super(WeatherView, self).get_size()
        return width, height - TOP_GRAPH

    def render(self, draw):
        super(WeatherView, self).render(self)
        # Clear area
        width,height=self.get_size()
        draw.rectangle((LEFT-2, TOP_GRAPH-2, width+4, TOP_GRAPH+height+4), fill=constants.WHITE, outline=constants.WHITE)
        # Show error if needed
        if self.weather is None:
            self.center_horizontally(TOP_TEMPERATURE, "unable to get forecast", fill=constants.BLACK, font=self.temp_font)
            return
        # Find highest and lowest of all forecasts
        low = 100
        high = -100
        for i, day in enumerate(self.weather.forecast):
            if day.low < low:
                low = day.low
            elif day.high > high:
                high = day.high
            if day.temperature < low:
                low = day.temperature
            elif day.temperature > high:
                high = day.temperature
        if low == high:
            high = high + 1
        # Draw forecasts
        for i in range(len(self.weather.forecast) - 1):
            day = self.weather.forecast[i]
            left = LEFT + i * (COLUMN_WIDTH + COLUMN_MARGIN)
            # Draw temperature
            #temp_str = u'{0}°'.format(str(round(day.temperature)))
            temp_str = str(int(round(day.temperature)))
            w,h = self.temp_font.getsize(temp_str)
            draw.text((left, TOP_TEMPERATURE), temp_str, fill=constants.BLACK, font=self.temp_font)
            draw.text((left + w, TOP_TEMPERATURE), u'°', fill=constants.BLACK, font=self.title_font)
            # Draw time
            if i == 0:
                draw.text((left, TOP_TIME), 'now', fill=constants.BLACK, font=self.title_font)
            else:
                draw.text((left, TOP_TIME), day.get_time(), fill=constants.BLACK, font=self.title_font)
            # Draw graphs
            self.draw_line(draw, day.temperature, self.weather.forecast[i+1].temperature, left, high, low, line_width=LINE_WIDTH)
            self.draw_line(draw, day.high, self.weather.forecast[i+1].high, left, high, low)
            self.draw_line(draw, day.low, self.weather.forecast[i+1].low, left, high, low)
            # Draw icon
            bitmap = self.get_icon(day)
            draw.bitmap((left, TOP_TIME + TEXT_SIZE_TIME), bitmap, fill=None)
    
    def draw_line(self, draw, temp1, temp2, left, high, low, line_width=1):
            """ Draws a part of the graph from one temperature
                to the next.
            """
            # Normalize to most extreme highs and lows
            factor1 = (temp1 - low) / (high - low)
            factor2 = (temp2 - low) / (high - low)
            x1 = left
            x2 = left + COLUMN_WIDTH + COLUMN_MARGIN
            # Flip (low y when high temp), stretch to graph
            # height, and shift to the right y-offset (TOP)
            y1 = TOP_GRAPH + (1 - factor1) * GRAPH_HEIGHT
            y2 = TOP_GRAPH + (1 - factor2) * GRAPH_HEIGHT
            draw.line((x1,y1,x2,y2), fill=constants.BLACK, width=line_width)

    def get_icon(self, day):
        """ Returns the icon for the conditions of the given day.
            Icon is loaded from the following locations (in order):
            1. ./assets/icons directory
            2. ../cache/ directory
            3. OpenWeatherMap api
        """
        file = ICON_PATH.format(day.icon_id)
        if os.path.isfile(file):
            im = Image.open(file)
            return im
        return self.threshold_bitmap(self.cached_bitmap(day.icon_url, day.icon_file, ICON_SIZE))
