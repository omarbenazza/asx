import requests
import json
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            try:
                error_content = json.loads(e.response.content)
                print(json.dumps(error_content, indent=4))
            except json.JSONDecodeError:
                print(e.response.content.decode())
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to create a VM
def create_vm(session_id, os):
    try:
        headers = {'vmware-api-session-id': session_id, 'Content-Type': 'application/json'}
        data = {

                "name": "asxtest",
                "guest_OS": os,
                "placement": {
                    "datastore": "datastore-14",
                    "folder": "group-v1010",
                    "resource_pool": "resgroup-10"
                },
                "hardware": {
                    "cpu": {
                        "count": 2
                    },
                    "memory": {
                        "size_MiB": 2048
                    },
                    "disks": [
                        {
                            "new_vmdk": {
                                "capacity": 20 * 1024 * 1024
                            }
                        }
                    ],
                    "nics": [
                        {
                            "network": "palo-to-vm",
                            "start_connected": True
                        }
                    ]
                }

        }

        response = requests.post(
            f"https://{VS_HOST}/rest/vcenter/vm",
            headers=headers,
            json=data,
            verify=False
        )
        response.raise_for_status()
        result = response.json()
        print(f"VM creation result: {json.dumps(result, indent=4)}")
        return True
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            try:
                error_content = json.loads(e.response.content)
                print(json.dumps(error_content, indent=4))
            except json.JSONDecodeError:
                print(e.response.content.decode())
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
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            try:
                error_content = json.loads(e.response.content)
                print(json.dumps(error_content, indent=4))
            except json.JSONDecodeError:
                print(e.response.content.decode())
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
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            try:
                error_content = json.loads(e.response.content)
                print(json.dumps(error_content, indent=4))
            except json.JSONDecodeError:
                print(e.response.content.decode())
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
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            try:
                error_content = json.loads(e.response.content)
                print(json.dumps(error_content, indent=4))
            except json.JSONDecodeError:
                print(e.response.content.decode())
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
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            try:
                error_content = json.loads(e.response.content)
                print(json.dumps(error_content, indent=4))
            except json.JSONDecodeError:
                print(e.response.content.decode())
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
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            try:
                error_content = json.loads(e.response.content)
                print(json.dumps(error_content, indent=4))
            except json.JSONDecodeError:
                print(e.response.content.decode())
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
