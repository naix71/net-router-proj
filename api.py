
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
            'ip': '192.168.10.27',
            'port': 32770,
            'username': 'admin',
            'password': 'eve123',
            'secret': 'eve123',
            'conn_timeout': 15,
            'auth_timeout': 15,
            'banner_timeout': 15,
        }

        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]

        net_connect = None

        try:
            print("Connecting to the router...")

            net_connect = ConnectHandler(**router_device)

            net_connect.enable()

            for cmd in commands_to_run:
                print(f"Executing: {cmd}")

                output = net_connect.send_command(
                    cmd,
                    read_timeout=60
                )

                result[cmd] = output

            print("Commands executed successfully.")

        except Exception as e:
            error = f"Connection or execution error: {e}"
            print(error)

        finally:
            if net_connect is not None:
                try:
                    net_connect.disconnect()
                    print("Disconnected from router.")
                except Exception as disconnect_error:
                    print(f"Disconnect warning: {disconnect_error}")

    return render_template(
        'index.html',
        result=result,
        error=error
    )

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )