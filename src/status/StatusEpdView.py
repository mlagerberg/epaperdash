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
from StatusView import StatusView

from PIL import ImageFont

FONT_SIZE = 16
MARGIN = 30
PADDING = 10

class StatusEpdView(StatusView):

    def __init__(self, epd):
        StatusView.__init__(self, epd)
        self.font = ImageFont.truetype(constants.FONT_FILE_BOLD, FONT_SIZE)

    def clear(self, draw):
        width,height = self.epd.size
        draw.rectangle((MARGIN, MARGIN, width-MARGIN, height-MARGIN), fill=constants.WHITE, outline=constants.WHITE)

    def render(self, draw):
        super(StatusView,self).render(self)
        width,height = self.get_size()
        if self.status != constants.STATE_IDLE:
            # black box
            draw.rectangle((MARGIN, MARGIN, width-MARGIN, height-MARGIN), fill=constants.BLACK, outline=constants.WHITE)
            # message
            if not self.message is None:
                draw.text((MARGIN+PADDING, MARGIN+PADDING), self.message, fill=constants.WHITE, font=self.font)
            # yes/no buttons
            str_yes = "Yes"
            str_no = "Cancel"
            if self.status == constants.STATE_SHUTDOWN_CONFIRM:
                str_yes = "Shut down"
            if self.status == constants.STATE_REBOOT_CONFIRM:
                str_yes = "Reboot"
            tw,th = draw.textsize(str_no, font=self.font)
            draw.text((MARGIN+PADDING, height-MARGIN-PADDING-th), str_yes, fill=constants.WHITE, font=self.font)
            draw.text((width-MARGIN-PADDING-tw, height-MARGIN-PADDING-th), str_no, fill=constants.WHITE, font=self.font)
