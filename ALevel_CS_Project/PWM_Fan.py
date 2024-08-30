import RPi.GPIO as GPIO
import time


class Fan:
    def __init__(self, fan_speed=0):
        self.fan_speed = fan_speed

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(13, GPIO.OUT)
        Frequency = 50
        self.DutyCycle = 0
        self.fan_speed = self.DutyCycle
        self.pwmFan = GPIO.PWM(13, Frequency)
        self.pwmFan.start(0)

    def fan_on(self):
        self.fan_speed = 100
        self.pwmFan.ChangeDutyCycle(self.fan_speed)

    def fan_off(self):
        self.fan_speed = 0
        self.pwmFan.ChangeDutyCycle(self.fan_speed)

    def change_speed(self):
        self.fan_speed = 0
        return self.fan_speed


fan = Fan()
fan.fan_on()
fan.fan_off()
fan.change_speed()

for i in range(0, 101, 20):
    current_fan_speed = fan.fan_speed + i
    if current_fan_speed > 100:
        current_fan_speed = 100
    fan.pwmFan.ChangeDutyCycle(current_fan_speed)
    time.sleep(3)
for j in range(100, 0, -20):
    current_fan_speed = j
    if current_fan_speed < 0:
        current_fan_speed = 0
    fan.pwmFan.ChangeDutyCycle(current_fan_speed)
    time.sleep(3)

