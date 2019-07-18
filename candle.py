# 2019, Raymond Blum <raygeeknyc@gmail.com>
# Candle - light from a bright flare, flicker, then fade

import time
import board
import analogio
import pulseio
import random
from digitalio import DigitalInOut, Direction
import adafruit_dotstar

SAMPLE_COUNT = 5
FLARE_THRESHOLD = 512
BRIGHTNESS_BASE = 8172
FLICKER_RANGE = 5120
FADE_DELAY_SECS = 0.01
FLICKER_DELAY_SECS = 0.4
FLAME_DURATION_SECS = 20
FADE_STEP = -50
FLARE_DELAY_SECS = 0.2

# Initialize analog input connected to photocell
photocell = analogio.AnalogIn(board.A0)
led = pulseio.PWMOut(board.A1)
progress_led = DigitalInOut(board.D13)
progress_led.direction = Direction.OUTPUT
status_led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)

# Return the average of a series of values ignoring the min and max values
def smooth_light_level(sample_count):
    total = 0
    min = 99999
    max = 0
    for i in range(sample_count):
        light_sample = photocell.value
        if light_sample > max:
            max = light_sample
        if light_sample < min:
            min = light_sample
        total += light_sample
    total -= min
    total -= max
    return int(total / (sample_count - 2))


progress_led.value = True
status_led[0] = (255, 255, 0)
time.sleep(FLICKER_DELAY_SECS)

print("setting level")
initial_level = smooth_light_level(10)
print("base level {}".format(initial_level))

progress_led.value = False
status_led[0] = (255, 0, 0)

while smooth_light_level(SAMPLE_COUNT) - initial_level < FLARE_THRESHOLD:
    if progress_led.value:
        progress_led.value = False
    else:
        progress_led.value = True
    time.sleep(FLARE_DELAY_SECS)

status_led[0] = (0, 255, 0)
progress_led.value = True

print("lit")
lit_at = time.monotonic()
sputter_at = lit_at + FLAME_DURATION_SECS

print("flickering")
while time.monotonic() < sputter_at:
    flicker = random.randint(-1 * FLICKER_RANGE, FLICKER_RANGE)
    led.duty_cycle = BRIGHTNESS_BASE + flicker
    time.sleep(FLICKER_DELAY_SECS)

print("fading")
# Slowly decrease the brightness
for fade in range(BRIGHTNESS_BASE, -1, FADE_STEP):
    led.duty_cycle = int(fade)
    time.sleep(FADE_DELAY_SECS)
    
status_led[0] = (30, 0, 60)
