import requests
import json
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# vSphere credentials and server
VS_HOST = "192.168.0.251"
VS_USER = "administrator@vsphere.local"
VS_PASSWORD = "Time4work!"

# API endpoint for creating a session
URL = f"https://{VS_HOST}/rest/com/vmware/cis/session"

# Function to get the session ID (token)
def get_vsphere_token():
    try:
        response = requests.post(URL, auth=(VS_USER, VS_PASSWORD), verify=False)
        response.raise_for_status()
        session_id = response.json()['value']
        print(f"Session ID (Token): {session_id}")
        return session_id
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to create a VM
def create_vm(session_id, os):
    try:
        headers = {'vmware-api-session-id': session_id, 'Content-Type': 'application/json'}
        data = {
            "guest_OS": os,  # Update with the appropriate OS
            "name": "asxtest",
            "placement": {
                "folder": "group-v1010",  # Update with your actual folder ID
                "resource_pool": "resgroup-10",  # Update with your actual resource pool ID
                "host": "192.168.0.250",  # Update with your actual host ID
                #"cluster": "cluster-01",  # Update with your actual cluster ID
                "datastore": "datastore-14"  # Update with your actual datastore ID
            },
            "hardware_version": "vmx-15",  # Update with the appropriate hardware version if needed
            "boot": {
                "type": "bios",  # or "efi"
                "efi_legacy_boot": False,
                "network_protocol": "ipv4",  # or "ipv6"
                "delay": 0,
                "retry": False,
                "retry_delay": 0,
                "enter_setup_mode": False
            },
            "boot_devices": [
                {
                    "type": "disk"  # or "cdrom", "network", etc.
                }
            ],
            "cpu": {
                "count": 2,
                "cores_per_socket": 1,
                "hot_add_enabled": False,
                "hot_remove_enabled": False
            },
            "memory": {
                "size_MiB": 2048,
                "hot_add_enabled": False
            },
            "disks": [
                {
                    "type": "new_vmdk",
                    "new_vmdk": {
                        "name": "disk1",
                        "capacity": 20 * 1024 * 1024,
                        "storage_policy": {
                            "policy": "policy-123"  # Update with your actual storage policy ID
                        }
                    }
                }
            ],
            "nics": [
                {
                    "type": "vmxnet3",  # or "e1000", "e1000e", etc.
                    "upt_compatibility_enabled": False,
                    "mac_type": "manual",
                    "mac_address": "00:50:56:XX:YY:ZZ",  # Update with your actual MAC address
                    "pci_slot_number": 160,
                    "wake_on_lan_enabled": True,
                    "backing": {
                        "type": "standard_portgroup",
                        "network": "palo-to-vm",  # Update with your actual network ID
                        "distributed_port": ""  # If using distributed port
                    },
                    "start_connected": True,
                    "allow_guest_control": True
                }
            ],
            "cdroms": [
                {
                    "type": "iso",
                    "backing": {
                        "type": "iso_file",
                        "iso_file": "[datastore1] iso/ubuntu.iso",  # Update with your actual ISO path
                        "device_access_type": "readOnly"
                    },
                    "start_connected": True,
                    "allow_guest_control": True
                }
            ],
            "floppies": [
                {
                    "backing": {
                        "type": "image_file",
                        "image_file": "[datastore1] floppies/dos.img"  # Update with your actual image file path
                    },
                    "start_connected": False,
                    "allow_guest_control": False
                }
            ],
            "parallel_ports": [
                {
                    "backing": {
                        "type": "file",
                        "file": "[datastore1] parallel/output.log"  # Update with your actual file path
                    },
                    "start_connected": False,
                    "allow_guest_control": False
                }
            ],
            "serial_ports": [
                {
                    "yield_on_poll": False,
                    "backing": {
                        "type": "network",
                        "network_location": "tcp://localhost:10000"  # Update with your actual network location
                    },
                    "start_connected": False,
                    "allow_guest_control": False
                }
            ],
            "sata_adapters": [
                {
                    "type": "sata",
                    "bus": 0,
                    "pci_slot_number": 32
                }
            ],
            "scsi_adapters": [
                {
                    "type": "pvscsi",
                    "bus": 0,
                    "pci_slot_number": 33,
                    "sharing": "noSharing"
                }
            ],
            "nvme_adapters": [
                {
                    "bus": 0,
                    "pci_slot_number": 34
                }
            ],
            "storage_policy": {
                "policy": "policy-123"  # Update with your actual storage policy ID
            }
        }

        response = requests.post(
            f"https://{VS_HOST}/rest/vcenter/vm",
            headers=headers,
            data=json.dumps(data),
            verify=False
        )
        response.raise_for_status()
        result = response.json()
        print(f"VM creation result: {json.dumps(result, indent=4)}")
        return True
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Function to list vSphere folders with their identifiers
def list_vsphere_folders(session_id):
    try:
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(
            f"https://{VS_HOST}/rest/vcenter/folder",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        folders = response.json()
        print(f"Folders: {json.dumps(folders, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to list vSphere clusters with their identifiers
def list_vsphere_clusters(session_id):
    try:
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(
            f"https://{VS_HOST}/rest/vcenter/cluster",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        clusters = response.json()
        print(f"Clusters: {json.dumps(clusters, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to list vSphere networks with their identifiers
def list_vsphere_networks(session_id):
    try:
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(
            f"https://{VS_HOST}/rest/vcenter/network",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        networks = response.json()
        print(f"Networks: {json.dumps(networks, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to list vSphere datastores with their identifiers
def list_vsphere_datastores(session_id):
    try:
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(
            f"https://{VS_HOST}/rest/vcenter/datastore",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        datastores = response.json()
        print(f"Datastores: {json.dumps(datastores, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to list vSphere resource pools with their identifiers
def list_vsphere_resource_pools(session_id):
    try:
        headers = {'vmware-api-session-id': session_id}
        response = requests.get(
            f"https://{VS_HOST}/rest/vcenter/resource-pool",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        resource_pools = response.json()
        print(f"Resource Pools: {json.dumps(resource_pools, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to connect to vSphere using pyVmomi
def get_vsphere_service_instance():
    context = ssl._create_unverified_context()
    si = SmartConnect(host=VS_HOST, user=VS_USER, pwd=VS_PASSWORD, sslContext=context)
    return si

# Function to list available guest OS types
def list_vsphere_guest_os(client):
    try:
        os_families = client.vcenter.Guest.OperatingSystemFamily.list()
        os_types = client.vcenter.Guest.OperatingSystem.list()

        print("Available Guest OS Families:")
        for family in os_families:
            print(f"- {family.name} ({family.id})")

        print("\nAvailable Guest OS Types:")
        for os in os_types:
            print(f"- {os.name} ({os.id})")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    token = get_vsphere_token()
    if token:
        print("Listing folders:")
        list_vsphere_folders(token)
        print("\nListing clusters:")
        list_vsphere_clusters(token)
        print("\nListing networks:")
        list_vsphere_networks(token)
        print("\nListing datastores:")
        list_vsphere_datastores(token)
        print("\nListing resource pools:")
        list_vsphere_resource_pools(token)

        print("\nCreating VM:")
        for os in ["UBUNTU_64"]:
            print("OS", os)
            if create_vm(token, os):
                break
