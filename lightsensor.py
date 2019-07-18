# 2019, Raymond Blum <raygeeknyc@gmail.com>
# Read a photosensor

import time
 
import board
import analogio
 
# Initialize analog input connected to photocell
photocell = analogio.AnalogIn(board.A0)
 
while True:
    # Read the photosensor value
    light_level = photocell.value

    # Print the value
    print('Photocell value: {0}'.format(light_level))
