#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Display WiFi and other system info
#
################################################################################

import logging
import os
import sys
import time

#### move this to __init__.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from lib.InfoPage import InfoPage
from lib.InfoDisplay import InfoDisplay


LOG_LEVEL = "DEBUG"

WIFI_PAGE_DWELL = 1 #5.0
CONN_PAGE_DWELL = 10.0
CPU_PAGE_DWELL = 1 # 3.0
MEMORY_PAGE_DWELL = 1 # 5.0

MAX_RENDER_RETRIES = 5
ROW_OFFSET = 11


class WiFiPage(InfoPage):
    def __init__(self):
        super().__init__()
        self.renderCount = 0

    def _renderDone(self):
        self.renderCount = 0
        self.done = True
        return WIFI_PAGE_DWELL

    def _checkRenderDone(self):
        if self.renderCount > MAX_RENDER_RETRIES:
            self.renderCount = 0
            self.done = True
            return WIFI_PAGE_DWELL
        self.renderCount += 1
        self.done = False
        return 0.1

    def render(self):
        logging.debug(f"{self.__class__.__name__} start")
        r = self.runCmd("/usr/bin/nmcli radio wifi")
        #### FIXME
        if r == "disabled":
            font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 16)
            s = "WiFi Disabled"
            self.draw.text((0, 0), s, font=font, fill=255)
        elif r == "enabled":
            r = self.runCmd("/usr/sbin/wpa_cli status")
            info = self._parseOutput(r, '=')
            row = 0
            self.draw.text((0, row), "WiFi Enabled", font=self.font, fill=255)
            self.draw.text((72, row), info['L0'].split()[-1][1:-1], font=self.font, fill=255)
            row += ROW_OFFSET
            if info['wpa_state'] == "DISCONNECTED":

                # device not currently connected, retry a few times
                self.draw.text((0, row), "DISCONNECTED", font=self.font, fill=255)
                row += ROW_OFFSET
                self.draw.text((0, row), info['address'], font=self.font, fill=255)
                row += ROW_OFFSET
                return self._checkRenderDone()
            elif info['wpa_state'] == "COMPLETED":
                # data connection is in place, device might not yet have IP address
                self.draw.text((0, row), f"{info['bssid']};  {info['mode']}", font=self.font, fill=255)
                row += ROW_OFFSET
                if 'ip_address' in info:
                    self.draw.text((0, row), f"{info['ip_address']}", font=self.font, fill=255)
                    row += ROW_OFFSET
                self.draw.text((0, row), f"{info['wpa_state']};  {info['freq']}", font=self.font, fill=255)
                row += ROW_OFFSET

                r = self.runCmd("/usr/sbin/iwgetid -m")
                self.draw.text((0, row), r.replace(" Mode:", "").strip(), font=self.font, fill=255)
                if 'wifi_generation' in info:
                    self.draw.text((112, row), f"  [{info['wifi_generation']}]", font=self.font, fill=255)
                row += ROW_OFFSET
                if info['mode'] == "AP":
                    logging.info("AP: TBD")
                elif info['mode'] == "station":
                    logging.info("STA: TBD")
                else:
                    self.draw.text((0, row), f"Unknown Mode:  {info['mode']}", font=self.font, fill=255)
                    row += ROW_OFFSET
            else:
                # normal flow is DISCONNECTED -> SCANNING -> COMPLETED
                # retry a few times
                self.draw.text((0, row), info['wpa_state'], font=self.font, fill=255)
                return _checkRenderDone()
        else:
            self.draw.text((0, row), "Radio State Unknown", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), r, font=self.font, fill=255)
            row += ROW_OFFSET
        logging.debug(f"{self.__class__.__name__} done")
        return self._renderDone()

class ConnectionPage(InfoPage):
    def _render(self, info):
        print(f"INFO: {info}")
        row = 0
        if info['IN-USE'] != '*':
            self.draw.text((0, row), "WiFi not in use", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"SSID: {info['SSID']}", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"Mode: {info['MODE']};  Chan: {info['CHAN']}", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"Signal: {info['SIGNAL']}%", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"Bars: {info['BARS'].count('_')}", font=self.font, fill=255)
            row += ROW_OFFSET
            return 1.0
        else:
            self.draw.text((0, row), f"SSID: {info['SSID']}", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"Mode: {info['MODE']};  Chan: {info['CHAN']}", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"Rate: {info['RATE']};  {info['SIGNAL']}%", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"RSSI: {info['RSSI']};  Bars: {info['BARS'].count('_')}", font=self.font, fill=255)
            row += ROW_OFFSET
            self.draw.text((0, row), f"Security: {info['SECURITY']}", font=self.font, fill=255)
            row += ROW_OFFSET
        return CONN_PAGE_DWELL
    
    def render(self):
        logging.debug(f"{self.__class__.__name__} start")
        r = self.runCmd("cat /proc/net/wireless")
        lines = r.splitlines()
        rssis = {}
        for indx, line in enumerate(lines):
            if indx in (0, 1):
                continue
            parts = line.split()
            rssis[parts[0][:-1]] = parts[3][:-1]
        if len(rssis) > 1:
            logging.warning(f"Unexpected RSSI values: {rssis}")
        print(f">>> {rssis}")

        r = self.runCmd("nmcli -t -m m device wifi list --rescan yes")
        lines = r.splitlines()
        groups = [lines[i:i + 9] for i in range(0, len(lines), 9)]
        infoList = []
        for group in groups:
            infoList.append({line.split(':', 1)[0]: line.split(':', 1)[1] for line in group})
        for info in infoList:
            dwell = self._render(info)
            self.displaySubpage(dwell)
        logging.debug(f"{self.__class__.__name__} done")
        return 0

class CpuPage(InfoPage):
    def render(self):
        logging.debug(f"{self.__class__.__name__} start")
        #### TODO add /proc/meminfo and df -k /
        row = 0
        r = self.runCmd("cat /sys/class/thermal/thermal_zone0/temp")
        temp = int(r) / 1000.0
        self.draw.text((0, row), f"Temp: {temp}\u00b0C", font=self.font, fill=255)
        row += ROW_OFFSET

        r = self.runCmd("/usr/bin/uptime -p")
        self.draw.text((0, row), r.strip(), font=self.font, fill=255)
        row += ROW_OFFSET

        r = self.runCmd("/usr/bin/cat /proc/loadavg")
        vals = r.split(' ')[0:-1]
        self.draw.text((0, row), " ".join(vals), font=self.font, fill=255)
        row += ROW_OFFSET
        logging.debug(f"{self.__class__.__name__} done")
        return CPU_PAGE_DWELL

class MemoryPage(InfoPage):
    def render(self):
        logging.debug(f"{self.__class__.__name__} start")
        r = self.runCmd("cat /proc/meminfo")
        info = self._parseOutput(r, ':')
        row = 0
        info['MemAvail'] = info['MemAvailable']
        for key in ('MemTotal', 'MemFree', 'MemAvail'):
            self.draw.text((0, row), f"{key}: {info[key]}", font=self.font, fill=255)
            row += ROW_OFFSET

        for mnt in ('/', '/run', '/run/user/1000'):
            r = self.runCmd(f"df -k {mnt} -h")
            info = r.splitlines()[1].split()
            vals = " ".join(val for val in info[1:5])
            self.draw.text((1, row), f"{mnt}: {vals}", font=self.font, fill=255)
            row += ROW_OFFSET
        logging.debug(f"{self.__class__.__name__} done")
        return MEMORY_PAGE_DWELL


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)
    pageFuncs = (WiFiPage(), ConnectionPage(), CpuPage(), MemoryPage())
    pfNames = ", ".join(pf.__class__.__name__ for pf in pageFuncs)
    logging.debug(f"Pages: {pfNames}")

    display = InfoDisplay(pageFuncs)
    display.displayPages()
    display.clear()
