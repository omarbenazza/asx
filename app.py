from flask import Flask, render_template, request, redirect, url_for, flash, session
import atexit
import ssl
import socket
from datetime import datetime
import db
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Initialize the database
db.init_db()

# vSphere connection details
VS_HOST = None
VS_USER = None
VS_PASSWORD = None
session_id = None

@app.route('/')
def index():
    vms = db.get_vms()
    return render_template('index.html', vms=vms)

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    global session_id, VS_HOST, VS_USER, VS_PASSWORD
    if request.method == 'POST':
        VS_HOST = request.form.get('host')
        VS_USER = request.form.get('username')
        VS_PASSWORD = request.form.get('password')
        try:
            # Try resolving the hostname first
            socket.gethostbyname(VS_HOST)
            # Authenticate to the API and get a session ID
            response = requests.post(
                f"{VS_HOST}/rest/com/vmware/cis/session",
                auth=(VS_USER, VS_PASSWORD),
                verify=False  # Disable SSL verification for simplicity
            )
            response.raise_for_status()
            session_id = response.json()['value']
            flash('Connected to vSphere successfully!', 'success')
            session['connected'] = True
        except socket.gaierror as e:
            flash(f'Address resolution error: {str(e)}', 'danger')
            session['connected'] = False
        except requests.HTTPError as e:
            flash(f'HTTP error: {str(e)}', 'danger')
            session['connected'] = False
        except Exception as e:
            flash(f'Failed to connect to vSphere: {str(e)}', 'danger')
            session['connected'] = False
        return redirect(url_for('index'))
    return render_template('connect.html')

@app.route('/create_vm', methods=['POST'])
def create_vm():
    if 'connected' in session and session['connected']:
        vm_name = request.form.get('vm_name')
        vm_cpu = int(request.form.get('vm_cpu'))
        vm_memory = int(request.form.get('vm_memory'))
        vm_guest_os = request.form.get('vm_guest_os')
        datacenter_name = request.form.get('datacenter')
        folder_name = request.form.get('folder')
        resource_pool_name = request.form.get('resource_pool')
        try:
            headers = {'vmware-api-session-id': session_id}
            data = {
                "spec": {
                    "name": vm_name,
                    "guest_OS": vm_guest_os,
                    "placement": {
                        "datacenter": datacenter_name,
                        "folder": folder_name,
                        "resource_pool": resource_pool_name
                    },
                    "hardware": {
                        "cpu": {
                            "count": vm_cpu
                        },
                        "memory": {
                            "size_MiB": vm_memory
                        }
                    }
                }
            }
            response = requests.post(
                f"{VS_HOST}/rest/vcenter/vm",
                headers=headers,
                json=data,
                verify=False  # Disable SSL verification for simplicity
            )
            response.raise_for_status()
            result = response.json()
            vm_id = result['value']
            flash(f'VM {vm_name} created successfully!', 'success')
            # Save VM details to the database
            db.add_vm(vm_name, 'created', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'N/A')  # Update 'N/A' with actual IP if retrievable
        except requests.HTTPError as e:
            flash(f'HTTP error: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Failed to create VM: {str(e)}', 'danger')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
