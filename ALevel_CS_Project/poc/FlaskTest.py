from crypt import methods
from LDR import Ldr
from Temperature_Humidity import TempHumidity
from OLED_Display import Oled
from Neopixel_LEDs import Neopixel
# from Distance_Sensor import DistanceSensor
# from PWM_Fan import Fan
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def base():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensor()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    dist = 20
    return render_template("base2.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)


@app.route('/ledcontrol', methods=["GET", "POST"])
def ledcontrol():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensor()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    led = Neopixel()
    print(led)
    led.set_colour(255, 0, 0)
    led.turn_led_on()
    if request.method == "GET":
        return render_template("LED_Control.html", LDR=LDR_value, temp=temp_val, humidity=humid_val)
    elif request.method == "POST":
        led_control = request.form["ledcontrol"]
        message = "Control LED"
        led1 = Neopixel()
        led1.set_colour(255, 0, 0)
        if led_control == "On":
            print(led_control)
            led1.turn_led_on()
        else:
            print(led_control)
            led1.turn_led_off()
        return render_template("LED_Control.html", message=message, LDR=LDR_value, temp=temp_val, humidity=humid_val)


@app.route('/oleddisplay', methods=["GET", "POST"])
def oled_display():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensor()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    if request.method == "GET":
        return render_template("OLED_Display.html",LDR=LDR_value, temp=temp_val, humidity=humid_val)
    elif request.method == "POST":
        text_to_display = request.form["text_to_display"]
        oled = Oled()
        oled.display_text(text_to_display)
        message = "Message Updated"
        return render_template("OLED_Display.html", message=message, LDR=LDR_value, temp=temp_val, humidity=humid_val)
    else:
        return "Unknown error"


@app.route('/pid')
def pid():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensor()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    return render_template("PID_Controller.html",LDR=LDR_value, temp=temp_val, humidity=humid_val)

@app.route('/index')
def index():
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True, host="192.168.1.71")
