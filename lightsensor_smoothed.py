# 2019, Raymond Blum <raygeeknyc@gmail.com>
# Read smoothed values from a photosensor

import time
 
import board
import analogio
 
# Initialize analog input connected to photocell
photocell = analogio.AnalogIn(board.A0)
 
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
    return int(total / (sample_count-2))

while True:
    # Read a series of photosensor values
    light_level = smooth_light_level(5)

    # Print the value
    print('Photocell value: {0}'.format(light_level))
