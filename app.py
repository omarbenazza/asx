from flask import Flask, render_template, request, redirect, url_for, flash, session
import atexit
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import ssl
import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# vSphere connection details
VS_HOST = None
VS_USER = None
VS_PASSWORD = None
si = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    global si, VS_HOST, VS_USER, VS_PASSWORD
    if request.method == 'POST':
        VS_HOST = request.form.get('host')
        VS_USER = request.form.get('username')
        VS_PASSWORD = request.form.get('password')
        try:
            # Try resolving the hostname first
            socket.gethostbyname(VS_HOST)
            # Disable SSL certificate verification
            context = ssl._create_unverified_context()
            # Try connecting to vSphere
            si = SmartConnect(host=VS_HOST, user=VS_USER, pwd=VS_PASSWORD, sslContext=context)
            atexit.register(Disconnect, si)
            flash('Connected to vSphere successfully!', 'success')
            session['connected'] = True
        except socket.gaierror as e:
            flash(f'Address resolution error: {str(e)}', 'danger')
            session['connected'] = False
        except vim.fault.InvalidLogin:
            flash('Invalid login credentials. Please check your username and password.', 'danger')
            session['connected'] = False
        except vim.fault.HostConnectFault as e:
            flash(f'Host connection fault: {str(e)}', 'danger')
            session['connected'] = False
        except Exception as e:
            flash(f'Failed to connect to vSphere: {str(e)}', 'danger')
            session['connected'] = False
        return redirect(url_for('index'))
    return render_template('connect.html')

@app.route('/create_vm', methods=['GET', 'POST'])
def create_vm():
    if request.method == 'POST' and 'connected' in session and session['connected']:
        vm_name = request.form.get('vm_name')
        try:
            content = si.RetrieveContent()
            datacenter = content.rootFolder.childEntity[0]
            vm_folder = datacenter.vmFolder
            resource_pool = datacenter.hostFolder.childEntity[0].resourcePool

            config = vim.vm.ConfigSpec(
                name=vm_name,
                memoryMB=1024,
                numCPUs=1,
                guestId='rhel7_64Guest',  # Adjust guest ID based on the OS you are deploying
                version='vmx-11'
            )

            task = vm_folder.CreateVM_Task(config=config, pool=resource_pool)
            task_info = task.info
            while task_info.state == vim.TaskInfo.State.running:
                task_info = task.info

            if task_info.state == vim.TaskInfo.State.success:
                flash(f'VM {vm_name} created successfully!', 'success')
            else:
                flash(f'Failed to create VM: {task_info.error.msg}', 'danger')
        except vmodl.MethodFault as error:
            flash(f'Caught vmodl fault: {error.msg}', 'danger')
        except Exception as e:
            flash(f'Caught exception: {str(e)}', 'danger')
        return redirect(url_for('index'))
    return render_template('create_vm.html')

if __name__ == '__main__':
    app.run(debug=True)
