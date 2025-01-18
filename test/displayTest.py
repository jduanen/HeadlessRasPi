import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Create the I2C interface
i2c = board.I2C()

# Create the SSD1306 OLED class
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display
oled.fill(0)
oled.show()

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.load_default()

# Draw some text
draw.text((0, 0), "Hello, World!", font=font, fill=255)

# Display image
oled.image(image)
oled.show()
