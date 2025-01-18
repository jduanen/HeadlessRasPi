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
    def __init__(self, blinks=0):
        #### TODO make this support other displays, and at different I2C addresses
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c)

        self.font = ImageFont.load_default()
        #### TODO figure out if I should make the mode parameter variable
        self.img = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.img)

        # blink the display a given number of times and clear display
        for i in range(blinks * 2):
            self.oled.fill(i % 2)
            self.oled.show()
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
        self.render()
        self.oled.image(self.img)
        self.oled.show()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()