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


from __future__ import print_function
import json
import os
import requests
from datetime import datetime

import constants
from Controller import Controller

BUTTON_REBOOT = constants.BUTTON_1
BUTTON_SHUTDOWN = constants.BUTTON_2


def reconnect():
    print("restarting network")
    os.system("service networking restart")

def shutdown():
    print("shutting down")
    os.system("halt")

def reboot():
    print("rebooting now")
    os.system("reboot")

class StatusController(Controller):
    """
    StatusController listens to button presses
    to initiate a shutdown or reboot action,
    and shows a confirmation dialog before
    doing so.

    Attributes:
        status      Current status (Idle, rebooting,
                    waiting for confirmation, etc.)
        has_changed Detects changes in state.
    """

    status = constants.STATE_IDLE
    has_changed = False


    def __init__(self, view):
        Controller.__init__(self, view)

    def on_click(self, button):
        old_status = self.status
        handled_event = False
        if self.status == constants.STATE_IDLE:
            # Change status from IDLE when buttons are pressed:
            if button == BUTTON_REBOOT:
                self.status = constants.STATE_REBOOT_CONFIRM
                handled_event = True
            elif button == BUTTON_SHUTDOWN:
                self.status = constants.STATE_SHUTDOWN_CONFIRM
                handled_event = True
        elif self.status == constants.STATE_REBOOT_CONFIRM:
            handled_event = True
            self.status = constants.STATE_REBOOTING if self.is_yes(button) else constants.STATE_IDLE
        elif self.status == constants.STATE_SHUTDOWN_CONFIRM:
            handled_event = True
            self.status = constants.STATE_SHUTTING_DOWN if self.is_yes(button) else constants.STATE_IDLE
        self.has_changed = old_status != self.status
        return handled_event

    def is_yes(self, button):
        """ The two leftmost buttons are 'Yes' buttons,
            the two rightmost buttons are 'No/Cancel' buttons.
        """
        return button == constants.BUTTON_1 or button == constants.BUTTON_2

    def update(self):
        self.view.cancel_full_update()
        self.view.set_status(self.status)
        result = self.has_changed
        self.has_changed = False
        return result

    def requests_exit(self):
        return self.status == constants.STATE_SHUTTING_DOWN or self.status == constants.STATE_REBOOTING

    def finish(self):
        """ Called once the main loop has been exited,
            which means we can start the shutdown.
        """
        if self.status == constants.STATE_SHUTTING_DOWN:
            shutdown()
        elif self.status == constants.STATE_REBOOTING:
            reboot()
