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
  - sudo apt install virtualenvwrapper python3-virtualenvwrapper
  - echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python" >> ~/.bashrc
    echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> ~/.bashrc
  - mkvirtualenv --python=`which python3` --prompt=wifi WIFI
  - workon WIFI
  - pip3 install adafruit-circuitpython-ssd1306
  - pip3 install pillow

# Use

* Select AP and Set WiFi Credentials
  - ?
* Display Text
  - ?
  - using the default font: six lines (with one or two lines of spacing) and 20 characters
* Flush WiFi Credentials
  - short pins 39 and 40 on the GPIO header for three or more seconds
    * bottom two pins, nearest to RJ45 connector
  - green LED on the front of the board will blink three times to confirm the flush has been done
* ?
