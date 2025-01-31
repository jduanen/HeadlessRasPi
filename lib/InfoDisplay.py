#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Information Display object for I2C OLED on RasPi
#
################################################################################

import logging
import os
import sys

#### move this to __init__.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from lib.InfoPage import InfoPage


class InfoDisplay():
    def __init__(self, pageFuncs):
        if not isinstance(pageFuncs, (list, tuple)) or (len(pageFuncs) < 1):
            logging.error("Must provide one or more page functions")
            raise ValueError("InfoPage list error")
        if not all(isinstance(pf, InfoPage) for pf in pageFuncs):
            logging.error("Not all members are InfoPage objects")
            raise ValueError("Invalid list of InfoPage functions")
        self.pageFuncs = pageFuncs
        self.currentPage = 0

    def clear(self):
        self.pageFuncs[self.currentPage].clear()

    def displayCurrentPage(self):
        self.pageFuncs[self.currentPage].display()

    def displayPage(self, pageNum):
        if (pageNum < 0) or (pageNum >= len(self.pageFuncs)):
            logging.error(f"Invalid page number: {pageNum}")
            raise ValueError("Invalid page number")
        self.currentPage = pageNum
        self.displayCurrentPage()

    def displayNextPage(self):
        self.currentPage += 1
        self.displayCurrentPage()

    def displayPages(self):
        for num in range(len(self.pageFuncs)):
            logging.debug(f"Display page #{num}")
            self.displayPage(num)
