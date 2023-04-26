import RPi.GPIO as GPIO
from flask import Flask, render_template
app = Flask(__name__)
pin = [5, 6, 13, 16, 19, 20, 21, 26]
IN_name_list   = ['IN1','IN2','IN3','IN4','IN5','IN6','IN7','IN8'] 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)

@app.route("/")  
def index():
    return render_template('index.html')

@app.route("/<Relay_Number>/<action>")  
def action(Relay_Number, action):
    for i in range(len(IN_name_list)):
        if Relay_Number == IN_name_list[i] :
            actuator = pin[i]
    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    elif action == "off":
        GPIO.output(actuator, GPIO.LOW)
    return render_template('index.html')

if __name__ == "__main__":
   app.run(host='192.168.50.4', port=443, debug=True)