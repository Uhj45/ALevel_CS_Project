from crypt import methods
from LDR import Ldr
from Temperature_Humidity import TempHumidity
from OLED_Display import Oled
from Neopixel_LEDs import Neopixel, Neopixel2
from Distance_Sensor import DistanceSensor
from PWM_Fan import Fan
import time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def base():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    distance = DistanceSensor()
    dist = distance.get_distance()
    return render_template("base2.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)


@app.route('/ledcontrol', methods=["GET", "POST"])
def ledcontrol():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    if request.method == "GET":
        return render_template("LED_Control.html", LDR=LDR_value, temp=temp_val, humidity=humid_val)
    elif request.method == "POST":
        led_control = request.form["Submit"]
        led1 = Neopixel2(brightness=1, phyiscal_led="LED1")
        led2 = Neopixel2(brightness=1, phyiscal_led="LED2")
        ledstatus1 = "Unknown"
        ledstatus2 = "Unknown"
        green = int(request.form["green"])
        red = int(request.form["red"])
        blue = int(request.form["blue"])
        print(f"{green}, {red}, {blue}")
        led1.set_colour(green, red, blue)
        led2.set_colour(green, red, blue)
        if led_control == "Submit":
            LED = request.form["LED"]
            control = request.form["Control"]
            if LED == "LED1":
                if control == "On":
                    ledstatus1 = "LED on"
                    print("LED 1 status: ", control)
                    led1.turn_led_on()
                elif control == "Off":
                    ledstatus1 = "LED off"
                    print("LED 1 status: ", control)
                    led1.turn_led_off()
            elif LED == "LED2":
                if control == "On":
                    ledstatus2 = "LED on"
                    print("LED 2 status: ", control)
                    led2.turn_led_on()
                elif control == "Off":
                    ledstatus2 = "LED off"
                    print("LED 2 status: ", control)
                    led2.turn_led_off()
        else:
            print("Not in use")
        return render_template("LED_Control.html", ledstatus1=ledstatus1, ledstatus2=ledstatus2, LDR=LDR_value, temp=temp_val, humidity=humid_val)


@app.route('/oleddisplay', methods=["GET", "POST"])
def oled_display():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
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
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()

    data = [
        ("01-01-2020", 1597),
        ("02-01-2020", 1456),
        ("03-01-2020", 1908),
        ("04-01-2020", 896),
        ("05-01-2020", 755),
        ("06-01-2020", 110),
        ("07-01-2020", 980),
     ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("PID_Controller.html", labels=labels, values=values, LDR=LDR_value, temp=temp_val, humidity=humid_val)


@app.route('/fancontrol', methods=["GET", "POST"])
def fan_control():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    print("Creating fan object")
    # fan1 = Fan()
    # print("Fan on")
    # fan1.set_speed(50)
    # time.sleep(5)
    if request.method == "GET":
        return render_template("Fan_Control.html", LDR=LDR_value, temp=temp_val, humidity=humid_val)
    elif request.method == "POST":
        fan_speed = request.form["fanspeed"]
        fan = Fan()
        fan.set_speed(fan_speed)
        time.sleep(5)
        return render_template("Fan_Control.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, fan_speed=fan_speed)

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
