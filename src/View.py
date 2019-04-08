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
from PIL import ImageFont
from PIL import Image
import urllib
import io
import os.path

CACHE_DIR = '../cache/{0}'
THRESHOLD = 245

def process_pixel_red(value):
    return 255 #if value > THRESHOLD else 0
def process_pixel_green(value):
    return 255 #if value > THRESHOLD else 0
def process_pixel_blue(value):
    return 255 if value > THRESHOLD else 0


class View(object):
    """
    Base View for each module. Compatible with
    E-paper displays (EPD) but can be used without.

    Attributes:
        update_fully    Used to track if the entire
                        E-paper display should be cleared.
    """

    update_fully = False

    def __init__(self, epd = None):
        """ Epd context can be omitted but is required
            when working with e-paper displays.
        """ 
        self.epd = epd
        
    def must_update_fully(self):
        return self.update_fully

    def cancel_full_update(self):
        self.update_fully = False

    def render(self, draw):
        """ Render this view to the Epd drawing context (or elsewhere,
            you can also print() to the console for example.)
        """
        return False

    def get_size(self):
        """ Size of the view in pixels, defaults to the entire
            EPD size.
        """
        if self.epd is None:
            raise ValueError('View does not have an EPD context')
        return self.epd.size

    def center_horizontally(self, draw, y, text, fill, font):
        """ Centers the given text horizontally and prints it,
            aligned to the given top
        """
        width,height = font.getsize(text)
        screenwidth,screenheight = self.epd.size
        x = (screenwidth - width) / 2
        draw.text((x, y), text, fill=fill, font=font)
        return x, y, width, height

    def download_file(self, url, target):
        """ Downloads file at {url} to file {target}.
            Warning: synchronous!
        """
        urllib.urlretrieve(url, target)

    def cached_file_path(self, url, filename):
        """ Checks for available files in the cache folder,
            and downloads the file if needed. Returns the
            full path to the file (in the cache dir).
            Does NOT check if existing cached files have
            expired.
        """
        path = CACHE_DIR.format(filename)
        if not os.path.isfile(path):
            print('Caching url {0} as {1}...'.format(url, path))
            self.download_file(url, path)
        return path

    def cached_bitmap(self, url, filename, size=None):
        """ Loads the file from the cache directory
            (downloading it if needed) and returns
            the bitmap.
        """
        path = self.cached_file_path(url, filename)
        im = Image.open(path)
        if not size is None:
            im.thumbnail(size)
        return im
        
    def threshold_bitmap(self, bitmap):
        bands = bitmap.split()
        red = bands[0].point(process_pixel_red)
        green = bands[1].point(process_pixel_green)
        blue = bands[2].point(process_pixel_blue)
        alpha = bands[3]
        return Image.merge("RGBA", (red, green, blue, alpha))
