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
        GPIO.output(self.pinTrigger, False)         # Sets the trigger pin to false
        time.sleep(0.5)                             # Gives the sensor has time to settle
        GPIO.output(self.pinTrigger, True)          # This done to get the trigger pulse and to get an echo response
        time.sleep(0.00001)                         # A sleep is put here to set the trigger pin to high for 10 milliseconds
        GPIO.output(self.pinTrigger, False)         # The trigger pin is set back to low again
        StartTime = None                            # The Start and stop time are initialised before the while loop
        StopTime = None
        while GPIO.input(self.pinEcho) == 0:        # This will record the first timestamp before the return signal is received
            StartTime = time.time()                 # This will get the first timestamp
        while GPIO.input(self.pinEcho):             # This while loop will get the last timestamp when the signal is high
            StopTime = time.time()                  # This will get the last timestamp once the signal has been received
            if StopTime - StartTime >= 0.04:        # Checks that the elapsed time is less than 0.04 otherwise the object is too close to the sensor
                print("That's really close")
                StopTime = StartTime

        ElapsedTime = StopTime - StartTime          # Calculates the elapsed time from the while loops above

        Distance = (ElapsedTime * 34326) / 2        # Calculates the distance that is going to be measured
        # Distance = Distance/2
        # time.sleep(0.5)
        return round(Distance, 2)                   # This returns the distance and rounds the value to two decimal places


