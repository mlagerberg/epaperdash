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

import locale
from datetime import datetime

DATE_FORMAT_LONG = "%a, %d %b %Y"
DATE_FORMAT = "%-d %B"
DAY_FORMAT = "%A"
#LOCALE = 'nl_NL'

class ClockView(View):
    """
    Simple View for date & time.
    Prints to the console only.
    """

    previous_minute = -1
    previous_day = -1

    def __init__(self, epd = None):
        View.__init__(self, epd)
        #locale.setlocale(locale.LC_ALL, LOCALE + '.utf8')

    def get_date_format(self):
        return DATE_FORMAT
        
    def get_day_format(self):
    	return DAY_FORMAT

    def render(self, draw):
        now = datetime.today()
        if now.day != self.previous_day:
            print(now.strftime(DATE_FORMAT))
            self.previous_day = now.day
        if now.minute != self.previous_minute:
            print('{h:02d}:{m:02d}'.format(h=now.hour, m=now.minute))

        self.update_fully = now.minute < self.previous_minute
        self.previous_minute = now.minute
