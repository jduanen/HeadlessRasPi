#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Display WiFi and other system info
#
################################################################################

import InfoPage
import InfoDisplay


class WiFiPage(InfoPage):
    def display(self):
        r = self.runCmd("/usr/bin/nmcli radio wifi")
        #### FIXME
        print(f"RESULT: {r}")

pageFuncs = (WiFiPage)

display = InfoDisplay(pageFuncs)

display.displayPages(2)
