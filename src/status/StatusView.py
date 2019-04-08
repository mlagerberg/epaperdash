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

class StatusView(View):

    def __init__(self, epd = None):
        View.__init__(self, epd)
        self.message = None
        self.status = constants.STATE_IDLE

    def set_status(self, state):
        if state == constants.STATE_IDLE and self.status != constants.STATE_IDLE:
            self.update_fully = True
        self.status = state
        if state == constants.STATE_SHUTDOWN_CONFIRM:
            self.message = "Shut down?"
        elif state == constants.STATE_REBOOT_CONFIRM:
            self.message = "Reboot?"
        elif state == constants.STATE_SHUTTING_DOWN:
            self.message = "Shutting down..."
        elif state == constants.STATE_REBOOTING:
            self.message = "Restarting..."
        else:
            self.message = None

    def render(self, draw):
        print("[rendering dialog]")
        if self.status != constants.STATE_IDLE:
            # message
            if not self.message is None:
                print(self.message)
            # yes/no buttons
            if self.status == constants.STATE_SHUTDOWN_CONFIRM or state == constants.STATE_REBOOT_CONFIRM:
                str_yes = "Yes"
                str_no = "Abort"
                print(str_yes)
                print(str_no)
