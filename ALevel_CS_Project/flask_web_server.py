from crypt import methods
from datetime import datetime
from sre_constants import error

from tabulate import tabulate
from LDR import Ldr
from Temperature_Humidity import TempHumidity
from OLED_Display import Oled
from Neopixel_LEDs import Neopixel, Neopixel2
from Distance_Sensor import DistanceSensor
from PWM_Fan import PCA9685Fan
from sql_database import StoreReadings
import time
from flask import Flask, render_template, request
from Algorthims import Schmitttrigger, ProportionalAlgorithm, ProportionalIntegralAlgorithm, PIDAlgorithm

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
    distance = DistanceSensor()
    dist = distance.get_distance()
    if request.method == "GET":
        return render_template("LED_Control.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)
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
    distance = DistanceSensor()
    dist = distance.get_distance()
    if request.method == "GET":
        return render_template("OLED_Display.html",LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)
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
    distance = DistanceSensor()
    dist = distance.get_distance()
    proportional_alg_selected = None
    integral_alg_selected = None
    derivative_alg_selected = None
    labels = None
    value1 = value2 = value3 = value4 = None
    scaled_fan_speed = None
    if request.method == "GET":
        return render_template("PID_Controller.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)
    elif request.method == "POST":
        print(request.form)
        parameter_list = request.form                         # Holds the key value pairs in a dictionary thats sent from the web form
        for key in parameter_list:                            # Goes through the dictionary and checks if the required keys for the PID constants are present
            if key == "P":
                proportional_alg_selected = request.form["P"]
                print(f"P: {proportional_alg_selected}")
            if key == "I":
                integral_alg_selected = request.form["I"]
                print(f"I: {integral_alg_selected}")

            if key == "D":
                derivative_alg_selected = request.form["D"]
                print(f"D: {derivative_alg_selected}")
        print(f"P: {proportional_alg_selected}, I: {integral_alg_selected}, D: {derivative_alg_selected}")

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
            duration = int(request.form["duration"])
            if proportional_alg_selected == "on" and (derivative_alg_selected != "on") and (integral_alg_selected != "on"):
                selected_algorithm = ProportionalAlgorithm(floats, target_height, Kp)
                selected_algorithm.get_config()
                selected_algorithm.run_proportional_algorithm(run_id,duration)
            elif proportional_alg_selected == "on" and integral_alg_selected == "on" and (derivative_alg_selected != "on"):
                selected_algorithm = ProportionalIntegralAlgorithm(floats, target_height, Kp, Ki)
                selected_algorithm.get_config()
                selected_algorithm.run_proportional_integral_algorithm(run_id, duration)
            elif proportional_alg_selected == "on" and integral_alg_selected == "on" and derivative_alg_selected == "on":
                selected_algorithm = PIDAlgorithm(floats, target_height, Kp, Ki, Kd)
                selected_algorithm.get_config()
            else:
                print("Invalid combination of algorithms")
            # pid_alg(run_id, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd)

        elif control_loop == "Schmitt Trigger":
            threshold = int(request.form["threshold"])
            duration = int(request.form["duration"])
            upper_threshold = target_height + threshold
            lower_threshold = target_height - threshold
            # schmitt_trigger_alg(run_id, target_height, threshold, upper_threshold, lower_threshold, floats, Kp, Ki, Kd)
            algorthim = Schmitttrigger(target_height, upper_threshold, lower_threshold)
            algorthim.schmitt_trigger_alg(target_height, upper_threshold, lower_threshold, threshold, run_id, floats, duration)

        data = get_values()
        # print(f"{data}, {type(data)}")
        labels = [row[1] for row in data]      # Time
        value1 = [row[0] for row in data]      # Actual measured height
        value2 = [row[2] for row in data]      # Target Height
        value3 = [row[3] for row in data]      # Upper Threshold
        value4 = [row[4] for row in data]      # Lower Threshold
        value5 = [row[5] for row in data]      # Fan speed
        value6 = [row[6] for row in data]      # Proportional constant
        value7 = [row[7] for row in data]      # Integral constant
        value8 = [row[8] for row in data]      # Derivative constant
        value9 = [row[9] for row in data]      # Proportional term
        value10 = [row[10] for row in data]    # Integral term
        value11 = [row[11] for row in data]    # Derivative term

        scaled_fan_speed = []
        # This scales down each value of the fan speed by a 1000 and adds to a list so that it can be plotted as a graph
        for i in value5:
            duty_cycle_scaled = i / 1000
            # print(f"{duty_cycle_scaled}")
            scaled_fan_speed.append(duty_cycle_scaled)

        scaled_p_constant = []
        for i in value6:
            p_constant_scaled = i / 1000
            scaled_p_constant.append(p_constant_scaled)
        scaled_p_term = []
        for i in value9:
            p_term_scaled = i / 1000
            scaled_p_term.append(p_term_scaled)

        scaled_i_term = []
        for i in value10:
            i_term_scaled = i / 100
            scaled_i_term.append(i_term_scaled)

        return render_template("PID_Controller.html",LDR=LDR_value,temp=temp_val,humidity=humid_val,labels=labels,value1=value1,value2=value2,value3=value3, value4=value4,value5=scaled_fan_speed,value6=scaled_p_constant,value7=value7,value8=value8,value9=scaled_p_term,value10=scaled_i_term,value11=value11)



@app.route('/plot_graphs', methods=["GET", "POST"])
def plot_graph():
    get_runid = StoreReadings()
    runid_values = get_runid.get_run_id()
    formatted_creation_date = []
    for plot_creation_time in runid_values:
        plot_creation_time = plot_creation_time[0]
        date_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.gmtime(plot_creation_time))
        formatted_creation_date.append(f"{date_time} {plot_creation_time}")
    if request.method == "GET":
        return render_template("plot_graph.html", runid_values=formatted_creation_date)
    elif request.method == "POST":
        graph = request.form["plot_graph"]
        if graph == "Plot Graph":
            time_stamp = request.form["runid"]
            print(time_stamp.split(" ")[1])
            runid = time_stamp.split(" ")[1]

            graph_data = StoreReadings()
            graph_dt = graph_data.get_graph_data(runid)
            epoch_time_graph = [row[1] for row in graph_dt]
            actual_height_graph = [row[0] for row in graph_dt]
            target_height_graph = [row[2] for row in graph_dt]
            upper_thresh_graph = [row[3] for row in graph_dt]
            lower_thresh_graph = [row[4] for row in graph_dt]
            fan_speed_graph = [row[5] for row in graph_dt]
            scaled_fan_speed = []
            for i in fan_speed_graph:
                duty_cycle_scaled = i / 1000
                # print(f"{duty_cycle_scaled}")
                scaled_fan_speed.append(duty_cycle_scaled)
        print(f"Date: {formatted_creation_date}")
        return render_template("plot_graph.html", runid_values=formatted_creation_date, Time_graph=epoch_time_graph, actual_height_graph=actual_height_graph, target_height_graph=target_height_graph, upper_thresh_graph=upper_thresh_graph, lower_thresh_graph=lower_thresh_graph, fan_speed_graph=scaled_fan_speed)


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
