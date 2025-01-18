#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Display WiFi and other system info
#
################################################################################

import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from lib.InfoPage import InfoPage
from lib.InfoDisplay import InfoDisplay


class WiFiPage(InfoPage):
    def render(self):
        r = self.runCmd("/usr/bin/nmcli radio wifi")
        #### FIXME
        print(f"RESULT: {r}")
        #### self.font = ImageFont.truetype(<path/font.ttf>, 16)
        self.draw.text((0, 0), r, font=self.font, fill=255)

pageFuncs = (WiFiPage(), )

display = InfoDisplay(pageFuncs)

display.displayPages(2)
