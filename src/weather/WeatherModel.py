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


from config import temperature_unit
from datetime import datetime
import tzlocal

KELVIN_ZERO = 273.15
ICON_URL = 'http://openweathermap.org/img/w/{0}.png'
ICON_FILENAME = '{0}.png'


def timezoneoffset():
    timezone = tzlocal.get_localzone()
    now = datetime.today()
    return timezone.utcoffset(now)

def fahrenheit2celsius(f):
    return round((f-32)/1.8)

def kelvin2celsius(k):
    return round(k - KELVIN_ZERO)

def kelvin2fahrenheit(k):
    return 9 * (k - KELVIN_ZERO) / 5 + 32


class Daily(object):
    """
    Forecast of one day.
    Also suitable for other time units,
    such as an hour or chunk of 3 hours.

    Attributes:
        condition       Human-readable description of weather
        temperature     Temperature, either in Celsius or Fahrenheit
                        depending on the setting in config.py
        high            Highest temperature in the timespan
        low             Lowest temperature
        icon_id         String id of the condition icon, e.g. "10d"
        icon_file       Filename (ex. path) of the icon
        icon_url        Online location of the icon
    """

    def __init__(self, response):
        self.condition = response['weather'][0]['description']
        if temperature_unit == 'c':
            self.temperature = kelvin2celsius(response['main']['temp'])
            self.high = kelvin2celsius(response['main']['temp_max'])
            self.low = kelvin2celsius(response['main']['temp_min'])
        else:
            self.temperature = kelvin2fahrenheit(response['main']['temp'])
            self.high = kelvin2fahrenheit(response['main']['temp_max'])
            self.low = kelvin2fahrenheit(response['main']['temp_min'])
        self.time = response['dt'] + timezoneoffset().seconds
        self.icon_id = response['weather'][0]['icon']
        self.icon_file = ICON_FILENAME.format(self.icon_id)
        self.icon_url = ICON_URL.format(self.icon_id)

    def get_time(self):
        dt = datetime.fromtimestamp(self.time)
        return '{h}:{m:02d}'.format(h=dt.hour, m=dt.minute)
        #return '{h}u'.format(h=dt.hour)


class WeatherModel(object):
    """
    Groups a bunch of Daily forecasts
    plus the current temperature

    Attributes:
        city        City name or nearest city name as determined
                    by the API based on the given location.
        temperature Current temperature
        forecast    List of forecasts of type Daily.
    """

    def __init__(self, response):
        self.city = response['city']['name']
        self.temperature = kelvin2celsius(response['list'][0]['main']['temp'])
        self.forecast = [ \
            Daily(response['list'][0]), \
            Daily(response['list'][1]), \
            Daily(response['list'][2]), \
            Daily(response['list'][3]), \
            Daily(response['list'][4]), \
            Daily(response['list'][5]), \
            Daily(response['list'][6])]
