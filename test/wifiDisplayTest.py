#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Display WiFi and other system info
#
################################################################################

import sys
import time
import os

#### move this to __init__.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from lib.InfoPage import InfoPage
from lib.InfoDisplay import InfoDisplay


DWELL_SECS = 5


class WiFiPage(InfoPage):
    def render(self):
        r = self.runCmd("/usr/bin/nmcli radio wifi")
        #### FIXME
        if r == "disabled":
            font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 16)
            s = "WiFi Disabled"
            self.draw.text((0, 0), s, font=font, fill=255)
        elif r == "enabled":
            '''
            wpa_cli status
            iwgetid -m
            if mode == Master:
                iw dev wlan0 info
                ?
            elif mode == ?:
                ?
            else:
                ?
            '''
            s = "WiFi Enabled"
            self.draw.text((0, 0), s, font=self.font, fill=255)
        else:
            s = "Other"
            self.draw.text((0, 0), s, font=self.font, fill=255)

class ConnectionPage(InfoPage):
    def render(self):
        self.draw.text((0, 0), "TBD", font=self.font, fill=255)

class CpuPage(InfoPage):
    def render(self):
        r = self.runCmd("/usr/bin/uptime")
        #### FIXME
        vals = r.split(',')
        #### self.font = ImageFont.truetype(<path/font.ttf>, 16)
        self.draw.text((0, 0), vals[0].strip(), font=self.font, fill=255)
        self.draw.text((0, 11), vals[2].strip(), font=self.font, fill=255)
        self.draw.text((0, 22), vals[3].strip(), font=self.font, fill=255)
        print(f"RESULT: {vals[0]}, {vals[2]}, {vals[3]}")
        #### TODO add cpu temp and /proc/meminfo and df -k /

pageFuncs = (WiFiPage(), ConnectionPage(), CpuPage())

display = InfoDisplay(pageFuncs)

display.displayPages(DWELL_SECS)

display.clear()