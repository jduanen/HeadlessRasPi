# HeadlessRasPi
WiFi Provisioning and Status Display for Headless Raspberry Pi

# Configuration

## Mini-Display Hardware Setup

### Add 0.96" OLED display

* connections
  - SDA: GPIO2 (pin 3)
  - SCL: GPIO3 (pin 5)
  - VCC: 3.3V  (pin 1)
  - GND: GND   (pin 14)

## Software Setup

### WiFi Provisioning

* install Comitup
  - ?
* patch NetworkManager.py
  - ?

### Display

* enable I2C on RasPi
  - 'sudo raspi-config'
    * Interface Options -> I2C: enable
  - reboot RasPi
* install libraries
  - sudo pip3 install adafruit-circuitpython-ssd1306
  - sudo pip3 install pillow

# Use

* Select AP and Set WiFi Credentials
  - ?
* Display Text
  - ?
* Flush WiFi Credentials
  - short pins 39 and 40 on the GPIO header for three or more seconds
    * bottom two pins, nearest to RJ45 connector
  - green LED on the front of the board will blink three times to confirm the flush has been done
* ?
