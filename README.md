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

### WiFi Provisioning SW Setup

* install Comitup
  - ?
* configure Comitup
  - ?
* patch NetworkManager.py
  - ?

### Display SW Setup

* enable I2C on RasPi
  - 'sudo raspi-config'
    * Interface Options -> I2C: enable
  - reboot RasPi

* install Python libraries in a venv
  - sudo apt install virtualenvwrapper python3-virtualenvwrapper
  - echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
  - echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python" >> ~/.bashrc
  - echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> ~/.bashrc
  - mkvirtualenv --python=`which python3` --prompt=wifi WIFI
  - workon WIFI
  - pip3 install -r requirements

# Use

* Select AP and Set WiFi Credentials
  - on any (desktop or mobile) browser, select the AP whose names starts with "comitup-"
  - doing a sign-in to the AP takes you to the comitup provisioning page
  - select the desired AP from the list, enter the passphrase, and click the "Connect" button
  - the raspi is now provisioned and should connect to the desired AP
    * if the wrong passphrase is given, the raspi will fall back and offer the AP named "comitup..." again
  - once connected to the AP, it should be possible to ssh into the raspi

* Flush WiFi Credentials
  - short pins 39 and 40 on the GPIO header for three or more seconds
    * bottom two pins, nearest to RJ45 connector
  - green LED on the front of the board will blink three times to confirm the flush has been done

* Information display 
  - if a display is attached, it should show pages of information whenever the state of the wifi link changes
  - it should be possible to apply power to the raspi and then see what the machine is doing, what the state of the wifi link is, and what APs the raspi can see
    * the signal strength, channel, frequency, and generation of WiFi are displayed when the raspi is connected to an AP
    * a subset of the WiFi link information is displayed when the raspi is offering the provisioning web page in AP mode

* ?

# Notes

* To disable the feature causing WiFi problems:
  - move brcmfmac.conf to /etc/modprobe.d/brcmfmac.conf
  - can see errors in journalctl -t kernel
  - the problem manifests itself as a long delay in setting up wifi connections

* Enable flushing the credentials with 'enable_nuke: 1' in /etc/comitup.conf
  - can also set 'verbose: <n>' if you want logs in /var/log/comitup.log and /var/log/comitup-web.log

* The comitup utility writes connection files to /etc/NetworkManager/system-connections/
  - comitup-<num>-<num'>.nmconnection: the 10.41.0.1 config address
    * [connection]->autoconnect flag set to 'false'
    * [ipv4]->method = manual
  - <SSID>.nmconnection: the connection that was provisioned via the web interface
    * this should show be chmod 600
    * this does not have the [connection]->autoconnect flag set to 'true'
      - it doesn't exist at all in this file
    * [ipv4]->method = auto

* Currently using the default font: six lines (with one or two lines of spacing) and 20 characters
  - can use a different font if it makes sense later
  - individual pages can use their own fonts

* if the display SW is installed and no display is attached, then a message will be logged
  - the log is tagged with 'systemDisplay' and is visible with 'journalctl -t systemDisplay'
  - the system display SW does not check if a device is connected and will fail if run without a display (or if the display is disconnected while it is running)

* The contents of the pages (and subpages) displayed, as well as the ordering and the amount of time each page is displayed, is configurable

* 
