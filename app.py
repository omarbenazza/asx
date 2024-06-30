from flask import Flask, render_template, request, redirect, url_for, flash, session
import atexit
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# vCenter connection details
VCENTER_HOST = None
VCENTER_USER = None
VCENTER_PASSWORD = None
si = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    global si, VCENTER_HOST, VCENTER_USER, VCENTER_PASSWORD
    if request.method == 'POST':
        VCENTER_HOST = request.form.get('host')
        VCENTER_USER = request.form.get('username')
        VCENTER_PASSWORD = request.form.get('password')
        try:
            si = SmartConnect(host=VCENTER_HOST, user=VCENTER_USER, pwd=VCENTER_PASSWORD)
            atexit.register(Disconnect, si)
            flash('Connected to vCenter successfully!', 'success')
            session['connected'] = True
        except Exception as e:
            flash(f'Failed to connect to vCenter: {str(e)}', 'danger')
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
