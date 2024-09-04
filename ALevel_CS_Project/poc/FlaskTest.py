from LDR import Ldr
from Temperature_Humidity import TempHumidity
# from OLED_Display import Oled
# from Distance_Sensor import DistanceSensor
# from PWM_Fan import Fan
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    return render_template("index.html", LDR=LDR_value, temp_val=temp_val, humid_val=humid_val)


# @app.route('/ldr')
# def ldr_test():
#     ldr = Ldr()
#     LDR_value = ldr.get_light_level()
#     return f"LDR value is: {LDR_value}"


# @app.route('/temp_humidity')
# def temp_humidity_test():
#     temp_humidity = TempHumidity()
#     temp_humidity.get_temperature()
#     #temp_humidity.get_humidity()
#     return f"Temperature: {temp_humidity.temperature} C" #Humidity: {temp_humidity.humidity} %"


# @app.route('/distance')
# def distance_test():
#     dist = 25
#     return f"Distance: {dist} cm"
#
#
# @app.route('/pwmfan')
# def pwmfan_test():
#     fan_speed = 100
#     return fan_speed
#
#

# @app.route('/oled')
# def oled_test():
#     display = Oled()
#     text = "Hello World"
#     oled = display.display_text(text)
#     return f"Message: {text}", oled

if __name__ == "__main__":
    app.run(debug=True, host="192.168.1.71")
