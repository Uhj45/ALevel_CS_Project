import RPi.GPIO as GPIO
import time


class DistanceSensor:
    """
    This class returns the distance of an object in front of the distance sensor.
    This is done by sending a pulse to the object and measures the time taken for it to bounce back.
    The trigger pin is driven LOW for 0.5 seconds and then driven HIGH for 10ms to start sending the pulses. The start time is noted
    The echo pin is monitored for a logic HIGH which indicates when a pulse has returned and the stop time is noted
    The calculated elapsed time is used to work out the distance of the object using the speed of sound in air
    """
    def __init__(self):
        """
        Initialises the GPIO pins for the distance sensor
        """
        self.distance = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pinTrigger = 17                   # attribute assigned to GPIO 17 pin on RPi
        self.pinEcho = 18                      # attribute assigned to GPIO 18 pin on RPi
        GPIO.setup(self.pinTrigger, GPIO.OUT)  # sets the trigger pin to be an output
        GPIO.setup(self.pinEcho, GPIO.IN)      # sets the echo pin to be an input

    def get_distance(self):
        """
        This function sends out pulses and listens for the bounced pulse to measure the distance of an object
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
            if StopTime - StartTime >= 0.04:        # If the time taken to send and receive the signal is below 0.04 which suggests that the object is really close to the sensor
                print("That's really close")
                StopTime = StartTime

        ElapsedTime = StopTime - StartTime          # Calculates the elapsed time from the while loops above

        Distance = (ElapsedTime * 34326) / 2        # Calculates the distance that is going to be measured
        return round(Distance, 2)                   # This returns the distance and rounds the value to two decimal places


