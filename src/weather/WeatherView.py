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

class WeatherView(View):

    def __init__(self, epd = None):
        View.__init__(self, epd)
        self.weather = None

    def set_weather(self, weather):
        self.weather = weather

    def render(self, draw):
        # Draw weather
        condition = None
        if not self.weather is None:
            # Titles & temperatures
            print(u'Current: %s°C' % str(self.weather.temperature))
            print(u'Today:   %s°C' % str(self.weather.forecast[0].temperature))
            # Condition
            condition = self.weather.forecast[0].condition
        else:
            condition = "unable to get forecast"
        # Draw condition
        print('Condition: %s' % condition)
