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


class Controller(object):
    """
    Base Controller for each module.

    Attributes:
        enabled         Toggles Controller on/off
        first_update    Helps triggering an update during
                        the first cycle
        view            The module's View
    """

    enabled = True
    first_update = True
    view = None

    def __init__(self, view = None):
        self.first_update = True
        self.last_update = datetime.now()
        if not view is None:
            self.set_view(view)

    def set_view(self, view):
        self.view = view
        self.first_update = True

    def get_view(self):
        return self.view
        
    def is_enabled(self):
        return self.enabled
        
    def enable(self):
        self.enabled = True
        
    def disable(self):
        self.enabled = False
        
    def on_click(self, button):
        """ Called when one of the HAT buttons are pressed """
        pass

    def update(self):
        """ Called on every cycle, allowing the Controller
            to refresh or update state.
            Should return True if state was updated (False if no changes)
            to trigger a View redraw.
        """
        return False

    def requests_exit(self):
        """ Should return True if controller
            wants the program to exit the main loop
        """
        return False

    def finish(self):
        """ Called after the main loop, when finishing up. Allows the
            Controller to release resources and clean up.
        """
        pass
