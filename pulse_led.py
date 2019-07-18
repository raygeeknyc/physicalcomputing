# 2019, Raymond Blum <raygeeknyc@gmail.com>
# Pulse an LED

import board
import pulseio

# Initialize PWM output connected to an LED
led = pulseio.PWMOut(board.A1)

print("pulsing")

while True:
    # Slowly increase the brightness
    for i in range(256):
        led.duty_cycle = int(i * 65535 / 255)
        time.sleep(0.01)

    # Slowly decrease the brightness
    for i in range(255, -1, -1):
        led.duty_cycle = int(i * 65535 / 255)
        time.sleep(0.01)

