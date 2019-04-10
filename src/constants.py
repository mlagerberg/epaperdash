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

import os

# Pixel colors
BLACK = 0
WHITE = 1

# Button IDs
BUTTON_NONE = 0
BUTTON_1 = 16
BUTTON_2 = 19
BUTTON_3 = 20
BUTTON_4 = 26

BUTTONS = [BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4]

LEDS = [6, 12, 5]

dirname = os.path.dirname(__file__)
FONT_FILE = os.path.join(dirname, 'assets/fonts/Coda-Regular.ttf')
FONT_FILE_BOLD = os.path.join(dirname, 'assets/fonts/Coda-ExtraBold.ttf')

STATE_IDLE = 1
STATE_SHUTDOWN_CONFIRM = 2
STATE_SHUTTING_DOWN = 3
STATE_REBOOT_CONFIRM = 4
STATE_REBOOTING = 5
