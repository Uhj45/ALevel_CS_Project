from Temperature_Humidity import TempHumidity
import time
readings = TempHumidity()  # Using the class TempHumidity, this creates the object for that class
readings.get_temperature_humidity()  # Calls method in the class
for i in range(0, 5):
    print(f"Temperature: {readings.temperature} °C", f"Humidity: {readings.humidity} %")
    time.sleep(1)