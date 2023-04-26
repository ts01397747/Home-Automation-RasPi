import RPi.GPIO as GPIO, os, subprocess
from base64 import b64encode

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
pins = [5, 6, 13, 16, 19, 20, 21, 26]
port = 443
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# Define function to generate button HTML code
def create_button(pin):
    state = GPIO.input(pin)
    if state:
        text = "on"
        color = "red"
    else:
        text = "off"
        color = "grey"
    return f'<button id="pin{pin}" style="background-color: {color}" onclick="toggle_pin({pin})">{text}</button>'

# Define HTML code for the webpage
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path+'/Relay.jpg', 'rb') as f:
    img_data = f.read()
    img_base64 = b64encode(img_data).decode('ascii')
html = f'''
<html>
<head>
    <title>Remote Relay Control Module with Siri Integration</title>
    <style>
        #relay-image {{
            max-width: 350px;
            height: auto;
            aspect-ratio: 4/3;
            margin-bottom: 20px;
        }}
        #gpio-container {{
            display: flex;
            justify-content: left;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: -230px;
            margin-bottom: 50px;
            width: 100%;
            max-width: 600px;
        }}
        .gpio-button {{
            width: 80vw;
            height: calc(40vw * 3 / 4);
            padding: 5%;
            border: none;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: grey;
            margin: 0;
        }}
        .gpio-button.on {{
            background-color: red;
        }}
        #reboot-button {{
            width: 80vw;
            height: calc(80vw * 3 / 4);
            padding: 5%;
            border: none;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: #3498db;
            margin: 0;
        }}
    </style>
    <script>
        function toggle_pin(pin) {{
            var button = document.getElementById("pin" + pin);
            if (button.innerText == "on") {{
                button.innerText = "off";
                button.style.backgroundColor = "grey";
            }} else {{
                button.innerText = "on";
                button.style.backgroundColor = "red";
            }}
            fetch("/toggle/" + pin);
        }}

    </script>
</head>
<body>
    <h2>Remote GPIO Relay Control API</h2>
    <h4>Server: <font color="green">ONLINE</font> firmware version <font color="green">3.0</font></h4>
    <img id="relay-image" src="data:image/jpg;base64,{img_base64}" alt="Relay">
    <div id="gpio-container">
        {''.join([create_button(pin) for pin in pins])}
    </div>

</body>
</html>
'''

# Define function to handle HTTP requests
def handle_request(environ, start_response):
    if environ['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-type', 'text/html')])
        return [html.encode()]
    elif environ['PATH_INFO'].startswith('/toggle/'):
        pin = int(environ['PATH_INFO'][len('/toggle/'):])
        state = GPIO.input(pin)
        GPIO.output(pin, not state)
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [f'Toggled pin {pin} to {not state}'.encode()]
    else:
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Not Found']

# Run the HTTP server
from wsgiref.simple_server import make_server
httpd = make_server('', port, handle_request)
print(f'Serving on port {port}...')
httpd.serve_forever()