from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    error = None

    if request.method == 'POST':
        router_device = {
            'device_type': 'cisco_ios_telnet',
            'ip': '192.168.10.84',
            'port': 32770,
            'username': 'admin',
            'password': 'eve123',
            'secret': 'eve123',
        }

        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]

        try:
            net_connect = ConnectHandler(**router_device)
            net_connect.enable()

            for cmd in commands_to_run:
                output = net_connect.send_command(cmd)
                result[cmd] = output

            net_connect.disconnect()

        except Exception as e:
            error = f"An error occurred: {e}"

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)