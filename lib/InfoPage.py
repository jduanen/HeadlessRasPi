#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Information Page object for use by InfoDisplay objects
#
################################################################################

import board
import digitalio
import logging
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod

import adafruit_ssd1306


class InfoPage(ABC):
    @staticmethod
    def _parseOutput(outStr, sepChar):
        #### TODO make sure sepChar is a char
        outDict = {}
        for indx, line in enumerate(outStr.splitlines()):
            if sepChar in line:
                k, v = line.split(sepChar)
                outDict[k.strip()] = v.strip()
            else:
                outDict[f"L{indx}"] = line
        return outDict

    def __init__(self):
        #### TODO make this support other displays, and at different I2C addresses
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c)

        self.font = ImageFont.load_default()
        #### TODO figure out if I should make the mode parameter variable
        self.img = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.img)

        self.clear()

    def runCmd(self, cmd):
        try:
            res = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
            result = res.strip()
        except subprocess.CalledProcessError as e:
            logging.warning(f"Command ({cmd}) failed with error: {e.output.strip()}")
            result = ""
        return result

    @abstractmethod
    def render(self):
        pass

    def display(self):
        while True:
            self.oled.fill(0)
            dwell = self.render()
            logging.debug(f"display: {dwell}")
            self.oled.image(self.img)
            self.oled.show()
            if dwell:
                time.sleep(dwell)
            else:
                break

    def fill(self, val):
        self.oled.fill(val)

    def showImg(self):
        self.oled.image(self.img)
        self.oled.show()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()
