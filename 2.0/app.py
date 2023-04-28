import RPi.GPIO as GPIO
from flask import Flask, render_template
app = Flask(__name__)
pin = [4, 22, 6, 26, 24, 25, 8, 7]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)
IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8 = [pin[i] for i in range(len(pin))]
IN1s = IN2s = IN3s = IN4s = IN5s = IN6s = IN7s = IN8s = 0
IN1_ = IN2_ = IN3_ = IN4_ = IN5_ = IN6_ = IN7_ = IN8_ = "OFF"
IN_num_list = [IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8] 
IN_num_list_str = ['IN1', 'IN2', 'IN3', 'IN4', 'IN5', 'IN6', 'IN7', 'IN8'] 
IN_s_list = [IN1s, IN2s, IN3s, IN4s, IN5s, IN6s, IN7s, IN8s] 
@app.route("/")
def index():
    for i in range(len(IN_s_list)):
        IN_s_list[i] = GPIO.input(IN_num_list[i])
    templateData = dict(zip((IN_num_list_str), IN_s_list))
    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    templateData = dict(zip((IN_num_list_str), IN_s_list))
    for i in range(len(IN_s_list)):
        if deviceName == IN_num_list_str[i]:
            actuator = IN_num_list[i]

    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    else:
        GPIO.output(actuator, GPIO.LOW)

    for i in range(len(IN_s_list)):
        IN_s_list[i] = GPIO.input(IN_num_list[i])

    return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='192.168.50.3', port=80, debug=True)
