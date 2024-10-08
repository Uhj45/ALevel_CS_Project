from crypt import methods
from datetime import datetime
from tabulate import tabulate
from LDR import Ldr
from Temperature_Humidity import TempHumidity
from OLED_Display import Oled
from Neopixel_LEDs import Neopixel, Neopixel2
from Distance_Sensor import DistanceSensor
from PWM_Fan import PCA9685Fan
from sql_database import StoreReadings, StorePidConstants
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
    # distance = DistanceSensor()
    # dist = distance.get_distance()
    return render_template("base2.html", LDR=LDR_value, temp=temp_val, humidity=humid_val)


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


def get_values():
    results = StoreReadings()
    return results.get_item()


def schmitt_trigger_alg(run_id, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd):
    results = StoreReadings()
    for i in range(0, 6):
        distance = DistanceSensor()
        height = distance.get_distance()
        results.add_item(run_id, height, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd)
        time.sleep(2)
    results.get_recent_record()



def pid_alg(run_id, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd):
    results = StoreReadings()
    for i in range(0, 6):
        distance = DistanceSensor()
        height = distance.get_distance()
        results.add_item(run_id, height, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd)
        time.sleep(2)
    results.get_recent_record()


@app.route('/get_data', methods=['GET'])
def get_data():
    data = get_values()
    print(f"This is my data: \n {tabulate(data, tablefmt='grid')}")
    return f"This is my data: \n {tabulate(data, tablefmt='grid')}"


@app.route('/pid', methods=["GET", "POST"])
def pid():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()

    if request.method == "GET":
        return render_template("PID_Controller.html", LDR=LDR_value, temp=temp_val, humidity=humid_val)
    elif request.method == "POST":
        print(request.form)
        parameter_list = request.form                         # Holds the key value pairs in a dictionary thats sent from the web form
        for key in parameter_list:                            # Goes through the dictionary and checks if the required keys for the PID constants are present
            # print(parameter_list.get(key))
            if key == "I":
                i = request.form["I"]
                # print(f"I is in the list: {'I' in key}")
                # print(f"{i}")
            if key == "P":
                p = request.form["P"]
                # print(f"P is in the list: {'P' in key}")
                # print(f"{p}")
            if key == "D":
                d = request.form["D"]
                # print(f"D is in the list: {'D' in key}")
                # print(f"{d}")
        control_loop = request.form["control_loop"]
        floats = request.form["floats"]
        target_height = int(request.form["height"])
        run_id = int(time.time())
        Kp = Ki = Kd = 0
        threshold = upper_threshold = lower_threshold = 0
        if control_loop == "PID":
            Kp = int(request.form["Kp"])
            Ki = int(request.form["Ki"])
            Kd = int(request.form["Kd"])
            pid_alg(run_id, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd)

        elif control_loop == "Schmitt Trigger":
            threshold = int(request.form["threshold"])
            upper_threshold = target_height + threshold
            lower_threshold = target_height - threshold
            schmitt_trigger_alg(run_id, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd)

        data = get_values()
        labels = [row[1] for row in data]
        value1 = [row[0] for row in data]
        return render_template("PID_Controller.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, labels=labels, value1=value1)


@app.route('/fancontrol', methods=["GET"])
def fan_control():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    print("Creating fan object")

    return render_template("Fan_Control.html", LDR=LDR_value, temp=temp_val, humidity=humid_val)


@app.route('/fan_control_on', methods=["POST"])
def fan_control_on():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    print(request.form)
    # fancontrol = request.form["fan_control"]
    fan_status = "On"
    pca_fan = PCA9685Fan()
    pca_fan.turn_fan_on()
    return render_template("Fan_Control.html", fan_status=fan_status, LDR=LDR_value, temp=temp_val, humidity=humid_val, fan_speed=100)


@app.route('/fan_control_off', methods=["POST"])
def fan_control_off():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    fan_status = "Off"
    pca_fan = PCA9685Fan()
    pca_fan.turn_fan_off()
    return render_template("Fan_Control.html", fan_status=fan_status, LDR=LDR_value, temp=temp_val, humidity=humid_val, fan_speed=100)


@app.route('/fan_control_speed', methods=["POST"])
def fan_control_speed():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    fan_speed = int(request.form["fanspeed"])
    pca_fan = PCA9685Fan()
    pca_fan.turn_fan_off()
    fan_status = "On"
    pca_fan.set_fan_speed(fan_speed)
    return render_template("Fan_Control.html", fan_status=fan_status, LDR=LDR_value, temp=temp_val, humidity=humid_val, fan_speed=fan_speed)


if __name__ == "__main__":
    app.run(debug=True, host="192.168.1.71")
