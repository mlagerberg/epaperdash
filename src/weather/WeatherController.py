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


import json
import requests
import os
from datetime import datetime, timedelta

from Controller import Controller
from WeatherModel import WeatherModel
from config import app_id, lat, lon

ROOT_URL = 'http://api.openweathermap.org/data/2.5/forecast'
CONDITIONS_URL = ROOT_URL + '?lat={1}&lon={2}&appid={0}'
# Paying API users may want to change 'daily' to 'hourly'
# for a more narrow grained graph.
FORECAST_URL = ROOT_URL + '/daily?lat={1}&lon={2}&appid={0}'

class WeatherController(Controller):
    """
    Controller that pulls weather information
    from OpenWeatherMap api.

    Attributes:
        last_update     Last update (so we don't pull too often)
        response        Api response
        weather         Weather model
        interval        The max interval between pulls (30 minutes)
        logger          Logger instance, logs to file and console.
    """

    last_update = datetime.now()
    response = None
    weather = None
    interval = timedelta(minutes = 30)

    def __init__(self, logger, view):
        Controller.__init__(self, view)
        self.logger = logger

    def fetch_weather(self):
    	global app_id, lat, lon
        try:
            # Get API response
            uri = CONDITIONS_URL.format(app_id, lat, lon)
            print('Uri: {0}'.format(uri))
            response = requests.get(uri)
            # Parse JSON
            data = json.loads(response.text)
            #print(data)
            if data is None:
                self.logger.warning('api returned error')
                return None
            if not 'list' in data:
                self.logger.warning('no weather conditions in response')
                return None
            return data
        except Exception as e:
            self.logger.exception(e)
            return None
       
    def update(self):
        has_changed = False
        now = datetime.now()
        if self.first_update:
            print("First update, fetching weather...")
            has_changed = True
            self.first_update = False
        #print("Last update: {0}, {1} ago".format(self.last_update, now - self.last_update))
        #print("Minimum interval: {0}".format(self.interval))
        if now - self.last_update > self.interval:
            print("Last update ({0}) too long ago: {1} > {2}".format(self.last_update, now - self.last_update, self.interval))
            has_changed = True
        if has_changed:
            self.last_update = now
            self.response = self.fetch_weather()
            # Update view
            if not self.response is None:
                self.weather = WeatherModel(self.response)
                self.view.set_weather(self.weather)
        return has_changed
