import RPi.GPIO as GPIO
import time


class DistanceSensor:
    def __init__(self, distance=None):
        """
        This parameter can have an optional value but not in this case
        :param distance:
        """
        self.distance = distance

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pinTrigger = 17
        self.pinEcho = 18
        GPIO.setup(self.pinTrigger, GPIO.OUT)
        GPIO.setup(self.pinEcho, GPIO.IN)
        self.StartTime = time.time()
        self.StopTime = 0

    def get_distance(self):
        GPIO.output(self.pinTrigger, False)
        time.sleep(0.5)
        GPIO.output(self.pinTrigger, True)
        time.sleep(0.00001)
        GPIO.output(self.pinTrigger, False)
        while GPIO.input(self.pinEcho) == 0:
            self.StartTime = time.time()
        while GPIO.input(self.pinEcho):
            self.StopTime = time.time()
            if self.StopTime - self.StartTime >= 0.04:
                print("That's really close")
                self.StopTime = self.StartTime
        ElapsedTime = self.StopTime - self.StartTime

        Distance = ElapsedTime * 34326
        Distance = Distance/2
        time.sleep(0.5)
        return Distance


