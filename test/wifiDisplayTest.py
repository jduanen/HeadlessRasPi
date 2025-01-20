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


DWELL_SECS = 15


class WiFiPage(InfoPage):
    @classmethod
    def _parseOutput(self, s):
        d = {}
        for indx, line in enumerate(s.splitlines()):
            if '=' in line:
                k, v = line.split('=')
                d[k] = v
            else:
                d[f"L{indx}"] = line
        return d

    def render(self):
        r = self.runCmd("/usr/bin/nmcli radio wifi")
        #### FIXME
        if r == "disabled":
            font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 16)
            s = "WiFi Disabled"
            self.draw.text((0, 0), s, font=font, fill=255)
        elif r == "enabled":
            r = self.runCmd("/usr/sbin/wpa_cli status")
            info = WiFiPage._parseOutput(r)
            '''
            lines = r.splitlines()
            ifName = lines[0].split()[2].strip()
            ifAddr = lines[1].split('=')[1]
            freq = lines[2].split('=')[1]
            ssid = lines[3].split('=')[1]
            mode = lines[5].split('=')[1]
            wpaState = lines[6].split('=')[1]
            ipAddr = lines[7].split('=')[1]
            '''
            self.draw.text((0, 0), "WiFi Enabled", font=self.font, fill=255)
            self.draw.text((72, 0), info[ifName[1:-1], font=self.font, fill=255)
            self.draw.text((0, 11), f"{ssid};  {mode}", font=self.font, fill=255)
            self.draw.text((0, 22), f"{ipAddr}; {wpaState}", font=self.font, fill=255)            
            self.draw.text((0, 33), f"{ifAddr};  {freq}", font=self.font, fill=255)
            if mode == "AP":
                print("AP")
                r = self.runCmd("/usr/sbin/iwgetid -m")
                self.draw.text((0, 44), r, font=self.font, fill=255)
            elif mode == "STA":
                print("STA")
            else:
                print("UNKNOWN Mode")
            '''
            if mode == Master:
                iw dev wlan0 info
                ?
            elif mode == ?:
                ?
            else:
                ?
            '''
        else:
            self.draw.text((0, 0), "Radio State Unknown", font=self.font, fill=255)

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