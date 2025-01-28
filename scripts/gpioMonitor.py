#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Script that will trigger the information display when a button is pushed
#
################################################################################

# N.B. documentation for gpiod: https://github.com/brgl/libgpiod/tree/master
#      and https://github.com/brgl/libgpiod/tree/master/bindings/python
from gpiod.line import Direction, Value
import subprocess

PIN_NUMBER = 20

chip = gpiod.Chip('/dev/gpiochip0')

lineConfig = {
    PIN_NUMBER: gpiod.LineSettings(direction=gpiod.line.Direction.INPUT,
                                   edge_detection=gpio.line.Edge.?,
                                   bias=gpiod.line.Bias.?,
                                   drive=Drive.PUSH_PULL,
                                   active_low=True,
#                                   debounce_period=?,
#                                   event_clock=?,

                                   )
}
line = chip.request_lines(lineConfig, lineConfig) 
line.request(consumer="gpio_monitor", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

while True:
    ev_line = line.event_wait(sec=1)
    if ev_line:
        event = line.event_read()
        if event.type == gpiod.LineEvent.FALLING_EDGE:
            subprocess.run(["/path/to/your/script.sh"])
