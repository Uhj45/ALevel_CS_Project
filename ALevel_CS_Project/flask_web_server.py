from datetime import datetime

from tabulate import tabulate
from LDR import Ldr
from Temperature_Humidity import TempHumidity
from OLED_Display import Oled
from Neopixel_LEDs import Neopixel, NeopixelLeds
from Distance_Sensor import DistanceSensor
from PWM_Fan import PwmFan
from sql_database import StoreReadings
import time
from flask import Flask, render_template, request
from Algorthims import Schmitttrigger, ProportionalAlgorithm, ProportionalIntegralAlgorithm, PIDAlgorithm

app = Flask(__name__)            # Initialises the Flask class and sets up the web application


def fetch_readings():
    """
    Fetches readings from all the sensors and stores them in a dictionary
    """
    sensor_readings = {}
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    distance = DistanceSensor()
    dist = distance.get_distance()

    sensor_readings["ldr"]         = {"ldr": LDR_value}
    sensor_readings["temperature"] = {"temperature": temp_val}
    sensor_readings["humidity"]    = {"humidity": humid_val}
    sensor_readings["distance"]    = {"distance": dist}

    return sensor_readings

def calc_x_axis_time_increments(list_of_epoch_times):
    """
    Each measurement is recorded with a timestamps in the database as an epoch which is a 16-digit number
    This function calculates the time difference for each measurement and is used for the x-axis on the graph
    :param list_of_epoch_times: takes in the list of epoch times that are stored in the database
    :return: a list of time increments that are then used for the x-axis on the graph
    """
    total = 0
    x_axis_increments = [0]
    for i in range(len(list_of_epoch_times) - 1):
        time_diff = list_of_epoch_times[i+1] - list_of_epoch_times[i]
        total = total + time_diff
        x_axis_increments.append(total)
    return x_axis_increments

@app.route('/')       # A route decorator that specifies the URL root endpoint
def base():
    """
    This creates objects for all the sensors and retrieves readings before returning them to an HTML webpage
    The HTML file for this route is passed in to the render_template function which displays the webpage when this
    endpoint is specified in the URL
    :return: rendered webpage
    """
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
    """
    This route controls the Neopixel LEDs.
    :return:
    """
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
        #
        led_control = request.form["Submit"]
        right_led = NeopixelLeds(brightness=1, phyiscal_led="RIGHT_LED")    # Creates an object for the right LED
        left_led = NeopixelLeds(brightness=1, phyiscal_led="LEFT_LED")    # Creates an object for the left LED
        right_led_status = "Unknown"
        left_led_status = "Unknown"
        green = int(request.form["green"])                        # The RGB values are retrieved
        red = int(request.form["red"])
        blue = int(request.form["blue"])
        print(f"{green}, {red}, {blue}")
        right_led.set_colour(green, red, blue)                         # Sets the colour for the right LED
        left_led.set_colour(green, red, blue)                         # Sets the colour for the left LED
        if led_control == "Submit":                               # Retrieves the rest of the
            LED = request.form["LED"]                             # Retrieves the LED that was selected
            control = request.form["Control"]                     # Retrieves the control (on/off) that was selected
            if LED == "RIGHT_LED":
                # Checks if the right LED was selected
                if control == "On":
                    # checks if either on or off was selected and turns the LED on or off
                    # The LED status is updated on the webpage
                    right_led_status = "LED on"
                    print("Right LED status: ", control)
                    right_led.turn_led_on()
                elif control == "Off":
                    right_led_status = "LED off"
                    print("Right LED status: ", control)
                    right_led.turn_led_off()
            elif LED == "LEFT_LED":
                # Checks if the right LED was selected
                if control == "On":
                    # checks if either on or off was selected and turns the LED on or off
                    # The LED status is updated on the webpage
                    left_led_status = "LED on"
                    print("Left LED status: ", control)
                    left_led.turn_led_on()
                elif control == "Off":
                    left_led_status = "LED off"
                    print("Left LED status: ", control)
                    left_led.turn_led_off()
        else:
            print("Not in use")
        return render_template("LED_Control.html", ledstatus1=right_led_status, ledstatus2=left_led_status,
                               LDR=LDR_value, temp=temp_val, humidity=humid_val)


@app.route('/oleddisplay', methods=["GET", "POST"])
def oled_display():
    """
    This controls the OLED display
    :return:
    """
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    distance = DistanceSensor()
    dist = distance.get_distance()
    if request.method == "GET":
        # This retrieves the sensor readings and displays them on the webpage
        return render_template("OLED_Display.html",LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)
    elif request.method == "POST":
        # This retrieves the input from the webpage and will present it on the OLED display
        text_to_display = request.form["text_to_display"]  # This retrieves the input and assigns it to this variable
        oled = Oled()                                      # The object for the Oled() class is created
        oled.display_text(text_to_display)                 # The method display_text() takes in the input from the webpage
                                                           # and displays on the OLED display
        message = "Message Updated"                        # This string is used to inform the user that new text has been sent to the display
        return render_template("OLED_Display.html", message=message, LDR=LDR_value, temp=temp_val, humidity=humid_val)
    else:
        return "Unknown error"


def get_values():
    results = StoreReadings()
    return results.get_item()

@app.route('/get_data', methods=['GET'])
def get_data():
    """
    This returns the entire database and structures it in a table format
    :return:
    """
    data = get_values()
    print(f"This is my data: \n {tabulate(data, tablefmt='grid')}")
    return f"This is my data: \n {tabulate(data, tablefmt='grid')}"


@app.route('/pid', methods=["GET", "POST"])
def pid():
    """
    This route triggers the PID and Schmitt Trigger algorithms
    :return:
    """
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
    if request.method == "GET":
        # This retrieves the sensor readings and displays them on the webpage
        return render_template("PID_Controller.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)
    elif request.method == "POST":
        # This gets all the input parameters from the webpage and runs the appropriate algorithm based on the parameters specified
        print(request.form)
        parameter_list = request.form     # Holds the key value pairs in a dictionary that's sent from the web form
        for key in parameter_list:        # Goes through the dictionary and checks if the required keys for the PID constants are present
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
        hover_foam = request.form["hover_foam"]
        target_height = int(request.form["height"])
        run_id = int(time.time())
        Kp = Ki = Kd = 0
        threshold = upper_threshold = lower_threshold = 0
        if control_loop == "PID":
            # Extracts all the parameters required for the PID algorithms
            Kp = int(request.form["Kp"])              # Proportional constant
            Ki = int(request.form["Ki"])              # Integral constant
            Kd = int(request.form["Kd"])              # Derivative constant
            duration = int(request.form["duration"])  # The duration for how long the algorithm runs for
            if proportional_alg_selected == "on" and (derivative_alg_selected != "on") and (integral_alg_selected != "on"):
                # Runs the proportional algorithm if only the proportional checkbox was selected
                # The required parameters for the algorithm are passed into the algorithm
                selected_algorithm = ProportionalAlgorithm(hover_foam, target_height, Kp)
                selected_algorithm.get_config()
                selected_algorithm.run_proportional_algorithm(run_id,duration)
            elif proportional_alg_selected == "on" and integral_alg_selected == "on" and (derivative_alg_selected != "on"):
                # Runs the proportional integral algorithm if only the proportional and integral checkbox was selected
                selected_algorithm = ProportionalIntegralAlgorithm(hover_foam, target_height, Kp, Ki)
                selected_algorithm.get_config()
                selected_algorithm.run_proportional_integral_algorithm(run_id, duration)
            elif proportional_alg_selected == "on" and integral_alg_selected == "on" and derivative_alg_selected == "on":
                # Runs the full PID algorithm if all the checkboxes were selected
                selected_algorithm = PIDAlgorithm(hover_foam, target_height, Kp, Ki, Kd)
                selected_algorithm.get_config()
                selected_algorithm.run_pid_algorithm(run_id, duration)
            else:
                print("Invalid combination of algorithms")

        elif control_loop == "Schmitt Trigger":
            # Extracts all the parameters required for the Schmitt Trigger
            threshold = int(request.form["threshold"])
            duration = int(request.form["duration"])
            # The upper and lower thresholds are calculated and passed into the schmitt trigger algorithm
            upper_threshold = target_height + threshold
            lower_threshold = target_height - threshold
            # The object for the Schmitt Trigger class is created and the
            algorithm = Schmitttrigger(target_height, upper_threshold, lower_threshold)
            algorithm.schmitt_trigger_alg(target_height, upper_threshold, lower_threshold, threshold, run_id, hover_foam, duration)

        data = get_values()                    # Retrieves all the values from the database with most recent runID
        # The code below assigns each variable to the appropriate list of values from the tuple
        labels = [row[1] for row in data]           # Time
        value1 = [row[0] * -1 for row in data]      # Actual measured height
        value2 = [row[2] * -1 for row in data]      # Target Height
        value3 = [row[3] * -1 for row in data]      # Upper Threshold
        value4 = [row[4] * -1 for row in data]      # Lower Threshold
        value5 = [row[5] for row in data]           # Fan speed
        value6 = [row[6] for row in data]           # Proportional constant
        value7 = [row[7] for row in data]           # Integral constant
        value8 = [row[8] for row in data]           # Derivative constant
        value9 = [row[9] for row in data]           # Proportional term
        value10 = [row[10] for row in data]         # Integral term
        value11 = [row[11] for row in data]         # Derivative term

        # Generates a meaningful title to display above the graph using the information about the control loop that was run
        graph_title = (f"Control Algorithm: {control_loop}, Target: {target_height}, Threshold: {threshold}, Kp: {Kp}, "
                       f"Ki: {Ki}, Kd: {Kd}, Time: {run_id}, Float: {hover_foam}")

        # Calculating the time increments using the list of epoch timestamps from the first column of the table
        x_axis_increments = calc_x_axis_time_increments(labels)

        scaled_fan_speed = []
        # This scales down each value of the fan speed by a 1000 and adds to a list so that it can be plotted as a graph
        for i in value5:
            duty_cycle_scaled = i / 1000
            # print(f"{duty_cycle_scaled}")
            scaled_fan_speed.append(duty_cycle_scaled)

        scaled_p_constant = []
        for i in value6:
            # This scales down each value of the Kp by a 1000 and adds to a list so that it can be plotted as a graph
            p_constant_scaled = i / 1000
            scaled_p_constant.append(p_constant_scaled)
        scaled_p_term = []
        for i in value9:
            # This scales down each value of the p term by a 1000 and adds to a list so that it can be plotted as a graph
            p_term_scaled = i / 1000
            scaled_p_term.append(p_term_scaled)

        scaled_i_term = []
        for i in value10:
            # This scales down each value of the i term by a 1000 and adds to a list so that it can be plotted as a graph
            i_term_scaled = i / 100
            scaled_i_term.append(i_term_scaled)

        print(tabulate(data))
        return render_template("PID_Controller.html",LDR=LDR_value,temp=temp_val,humidity=humid_val,
                               labels=x_axis_increments,value1=value1,value2=value2,value3=value3, value4=value4,
                               value5=scaled_fan_speed,value6=scaled_p_constant,value7=value7,value8=value8,
                               value9=scaled_p_term,value10=scaled_i_term,value11=value11,graph_title=graph_title)

@app.route('/plot_graphs', methods=["GET", "POST"])
def plot_graph():
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    distance = DistanceSensor()
    dist = distance.get_distance()

    # return render_template("base2.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)

    get_runid = StoreReadings()                  # An object of the StoreReadings() class is created
    runid_values = get_runid.get_run_id()        # Retrieves all the runID values from the database
    formatted_creation_date = []
    for plot_creation_time in runid_values:
        # Goes through all the runIDs and converts them to a YYYY-MM-DD_HH:MM:SS format which is easier to read and remember
        plot_creation_time = plot_creation_time[0]
        date_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.gmtime(plot_creation_time))
        formatted_creation_date.append(f"{date_time} {plot_creation_time}")
    if request.method == "GET":
        return render_template("plot_graph.html", runid_values=formatted_creation_date, LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)
    elif request.method == "POST":
        # The selected timestamp from the webpage is used to retrieve matching data from the database and is plotted
        graph = request.form["plot_graph"]
        if graph == "Plot Graph":
            time_stamp = request.form["runid"]
            print(time_stamp.split(" ")[1])
            runid = time_stamp.split(" ")[1]

            # The code here is reused from when plotting the graph after the algorithm has run
            # The same class is created by a different object
            graph_data = StoreReadings()
            graph_dt = graph_data.get_graph_data(runid)
            epoch_time_graph = [row[1] for row in graph_dt]
            actual_height_graph = [row[0] * -1 for row in graph_dt]
            target_height_graph = [row[2] * -1 for row in graph_dt]
            upper_thresh_graph = [row[3] * -1 for row in graph_dt]
            lower_thresh_graph = [row[4] * -1 for row in graph_dt]
            fan_speed_graph = [row[5] for row in graph_dt]
            p_constant_graph = [row[6] for row in graph_dt]
            i_constant_graph = [row[7] for row in graph_dt]
            d_constant_graph = [row[8] for row in graph_dt]
            p_term_graph = [row[9] for row in graph_dt]
            i_term_graph = [row[10] for row in graph_dt]
            d_term_graph = [row[11] for row in graph_dt]

            x_axis_increments = calc_x_axis_time_increments(epoch_time_graph)

            # In order to generate a meaningful graph title from the stored data the threshold is calculated and checked if its negative
            # If negative the PID was used otherwise the Schmitt algorithm was used
            if upper_thresh_graph[0]-target_height_graph[0] < 0:
                algorithm = "PID"
                threshold = 0
            else:
                algorithm = "Schmitt"
                threshold = upper_thresh_graph[0]-target_height_graph[0]

            graph_title = (f" Control Loop: {algorithm}, Target: {target_height_graph[0]}, Threshold: {threshold}, "
                           f"Kp: {p_constant_graph[0]}, Ki: {i_constant_graph[0]}, Kd: {d_constant_graph[0]}, Time: {epoch_time_graph[0]}")

        # The fan speed, and all the PID terms and constants are scaled down so they can be plotted on the graph
            scaled_fan_speed = []
            for i in fan_speed_graph:
                duty_cycle_scaled = i / 1000
                # print(f"{duty_cycle_scaled}")
                scaled_fan_speed.append(duty_cycle_scaled)

            scaled_p_constant = []
            for i in p_constant_graph:
                p_constant_scaled = i / 1000
                scaled_p_constant.append(p_constant_scaled)

            scaled_p_term = []
            for i in p_term_graph:
                p_term_scaled = i / 1000
                scaled_p_term.append(p_term_scaled)

            scaled_i_term = []
            for i in i_term_graph:
                i_term_scaled = i / 100
                scaled_i_term.append(i_term_scaled)

            print(tabulate(graph_dt))
            return render_template("plot_graph.html", runid_values=formatted_creation_date,
                                   Time_graph=x_axis_increments, actual_height_graph=actual_height_graph,
                                   target_height_graph=target_height_graph, upper_thresh_graph=upper_thresh_graph,
                                   lower_thresh_graph=lower_thresh_graph, fan_speed_graph=scaled_fan_speed,
                                   p_constant_graph=scaled_p_constant, i_constant_graph=i_constant_graph,
                                   d_constant_graph=d_constant_graph, p_term_graph=scaled_p_term,
                                   i_term_graph=scaled_i_term, d_term_graph=d_term_graph, graph_title=graph_title,
                                   LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)


@app.route('/fancontrol', methods=["GET"])
def fan_control():
    """
    This route retrieves all the sensor readings and displays them on the webpage
    :return:
    """
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    distance = DistanceSensor()
    dist = distance.get_distance()
    print("Creating fan object")

    return render_template("Fan_Control.html", LDR=LDR_value, temp=temp_val, humidity=humid_val, dist=dist)


@app.route('/fan_control_on', methods=["POST"])
def fan_control_on():
    """
    This route turns the fan on when the on button is clicked in the webpage
    :return:
    """
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    print(request.form)
    # fancontrol = request.form["fan_control"]
    fan_status = "On"            # This variable is assigned to a string that prints the status of the fan on the webpage
    pca_fan = PwmFan()
    pca_fan.turn_fan_on()
    return render_template("Fan_Control.html", fan_status=fan_status, LDR=LDR_value,
                           temp=temp_val, humidity=humid_val, fan_speed=100)


@app.route('/fan_control_off', methods=["POST"])
def fan_control_off():
    """
    This route turns on the fan off when the off button is clicked in the webpage
    :return:
    """
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    fan_status = "Off"          # This variable is assigned to a string that prints the status of the fan on the webpage
    pca_fan = PwmFan()
    pca_fan.turn_fan_off()
    return render_template("Fan_Control.html", fan_status=fan_status, LDR=LDR_value,
                           temp=temp_val, humidity=humid_val, fan_speed=100)


@app.route('/fan_control_speed', methods=["POST"])
def fan_control_speed():
    """
    This route sets the percentage speed of the fan depending on the value entered
    :return:
    """
    ldr = Ldr()
    LDR_value = ldr.get_light_level()
    temp_humidity = TempHumidity()
    temp_humidity.read_sensors()
    temp_val = temp_humidity.get_temperature()
    humid_val = temp_humidity.get_humidity()
    fan_speed = int(request.form["fanspeed"])
    pca_fan = PwmFan()
    pca_fan.turn_fan_off()     # Turns the fan off before setting it to the new speed
    fan_status = "On"          # This variable is assigned to a string that prints the status of the fan on the webpage
    pca_fan.set_fan_speed(fan_speed)
    return render_template("Fan_Control.html", fan_status=fan_status, LDR=LDR_value,
                           temp=temp_val, humidity=humid_val, fan_speed=fan_speed)

@app.route('/api/v1/ldr', methods=["GET"])
def ldr_api():
    """
    This route returns the latest ldr value as JSON string
    http://IP_address:port_number/api/v1/ldr
    :return: {"ldr": 2011}
    """
    return fetch_readings()["ldr"]

@app.route('/api/v1/temperature', methods=["GET"])
def temperature_api():
    """
    This route returns the latest temperature value as JSON string
    http://IP_address:port_number/api/v1/temperature
    :return:{"temperature": 24.9}
    """
    return fetch_readings()["temperature"]

@app.route('/api/v1/humidity', methods=["GET"])
def humidity_api():
    """
    This route returns the latest humidity value as JSON string
    http://IP_address:port_number/api/v1/humidity
    :return: {"humidity": 50}
    """
    return fetch_readings()["humidity"]

@app.route('/api/v1/distance', methods=["GET"])
def distance_api():
    """
    This route returns the latest distance value as JSON string
    http://IP_address:port_number/api/v1/distance
    :return: {"distance": 20.85}
    """
    return fetch_readings()["distance"]

@app.route('/api/v1/fanspeed/set_state', methods=["GET"])
def set_fan_speed_state_api():
    """
    This route returns the latest fan speed value as JSON string
    http://IP_address:port_number/api/v1/fanspeed/set_state?state=on
    :return: {"state": "on"}
    """
    state = request.args.get('state')
    pca_fan = PwmFan()
    if state.lower() == "on":
        pca_fan.set_fan_speed(100)
    elif state.lower() == "off":
        pca_fan.set_fan_speed(0)
    else:
        state = "ERROR, invalid state requested"

    return {"state": state}

@app.route('/api/v1/setfanspeed/', methods=["GET"])
def fan_speed_api():
    """
    This route returns the latest fan speed value as JSON string
    http://IP_address:port_number/api/v1/setfanspeed?raw_value=true&speed=65
    :return: {"fan_speed": "65", "raw_speed": "true"}
    """
    raw_speed = request.args.get('raw_value')
    value = request.args.get('speed')

    pca_fan = PwmFan()
    if raw_speed == 'true':
        pca_fan.set_raw_fan_speed(int(value))
    else:
        pca_fan.set_fan_speed(int(value))

    return {"raw_speed":raw_speed, "fan_speed": value}


@app.route('/api/v1/status', methods=["GET"])
def status_api():
    """
    http://IP_address:port_number/api/v1/status
    :return: Returns all sensor readings as a list {
        "distance": {
        "distance": 22.31
      },
      "humidity": {
        "humidity": 33.3
      },
      "ldr": {
        "ldr": 1996
      },
      "temperature": {
        "temperature": 25.0
      }
    }
    """
    return fetch_readings()

# The code below starts the web server and the IP address can be visited to access the webpages
if __name__ == "__main__":
    app.run(debug=True, host="192.168.1.71")
