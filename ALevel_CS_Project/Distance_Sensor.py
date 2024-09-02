import RPi.GPIO as GPIO
import time


class DistanceSensor:
    def __init__(self):
        """
        Initialises the GPIO pins for the distance sensor
        """
        self.distance = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pinTrigger = 17
        self.pinEcho = 18
        GPIO.setup(self.pinTrigger, GPIO.OUT)
        GPIO.setup(self.pinEcho, GPIO.IN)

    def get_distance(self):
        """

        :return: float value representing the distance from a surface object
        """
        GPIO.output(self.pinTrigger, False)
        time.sleep(0.5)
        GPIO.output(self.pinTrigger, True)
        time.sleep(0.00001)
        GPIO.output(self.pinTrigger, False)
        StartTime = None
        StopTime = None
        while GPIO.input(self.pinEcho) == 0:
            StartTime = time.time()
        while GPIO.input(self.pinEcho):
            StopTime = time.time()
            if StopTime - StartTime >= 0.04:
                print("That's really close")
                StopTime = StartTime
        ElapsedTime = StopTime - StartTime

        Distance = ElapsedTime * 34326
        Distance = Distance/2
        time.sleep(0.5)
        return Distance


