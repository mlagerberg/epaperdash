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


from Controller import Controller
from datetime import datetime

class ClockController(Controller):
    """
    Controller for the date and time display.
    """

    previous_minute = -1

    def __init__(self, view):
        Controller.__init__(self, view)
        self.previous_minute = -1

    def update(self):
        """ Update clock only once every minute
        """
        now = datetime.today()
        refresh = now.minute != self.previous_minute
        self.previous_minute = now.minute
        return refresh
