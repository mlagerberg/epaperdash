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
from ClockView import ClockView

from datetime import datetime
from PIL import ImageFont


CLOCK_FONT_SIZE = 40
DATE_FONT_SIZE = 16
HEIGHT = 50
TOP = 5

class ClockEpdView(ClockView):
    """
    Shows the current time as a 24-hr clock,
    plus the current date.

    Attributes:
        date_font       Small font for date
        clock_font      Large font for time
        previous_width  Helps clearing the area of the
                        clock as it looked the previous
                        minute
    """

    date_font = ImageFont.truetype(constants.FONT_FILE, DATE_FONT_SIZE)
    clock_font = ImageFont.truetype(constants.FONT_FILE, CLOCK_FONT_SIZE)
    previous_width = 0

    def __init__(self, epd):
        ClockView.__init__(self, epd)
        
    def get_size(self):
       	width,height = super(ClockView, self).get_size()
       	return width, HEIGHT

    def render(self, draw):
        super(ClockView, self).render(self)
        now = datetime.today()
        width, height = self.get_size()
        if now.minute != self.previous_minute:
            text = '{h:02d}:{m:02d}'.format(h=now.hour, m=now.minute)
            if now.day != self.previous_day:
                # Full refresh
                draw.rectangle((2, 2, width - 2, height + TOP - 2), fill=constants.WHITE, outline=constants.WHITE)
            else:
                # Partial refresh
                x = (width - self.previous_width) / 2
                draw.rectangle((x, TOP, x + self.previous_width, TOP + CLOCK_FONT_SIZE), fill=constants.WHITE, outline=constants.WHITE)
            # Draw clock
            x,y,w,h = self.center_horizontally(draw, TOP, text, fill=constants.BLACK, font=self.clock_font)
            self.previous_width = w
            # Draw date
            if now.day != self.previous_day:
                draw.text((x + w + 10, TOP + 7), now.strftime(self.get_date_format()), fill=constants.BLACK, font=self.date_font)
                draw.text((x + w + 10, TOP + 7 + DATE_FONT_SIZE), now.strftime(self.get_day_format()), fill=constants.BLACK, font=self.date_font)
                self.previous_day = now.day
        self.update_fully = now.minute < self.previous_minute
        self.previous_minute = now.minute
