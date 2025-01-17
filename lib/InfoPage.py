#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Information Page object for use by InfoDisplay objects
#
################################################################################

import logging
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod


class InfoPage(ABC):
    def __init__(self, oled):
        self.oled = oled

    def runCmd(self, cmd):
        try:
            res = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
            result = res.strip()
        except subprocess.CalledProcessError as e:
            logging.warning(f"Command ({cmd}) failed with error: {e.output.strip()}")
            result = ""
        return result

    @abstractmethod
    def display(self):
        pass
