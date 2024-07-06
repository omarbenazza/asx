import requests
import json
from com.vmware.vsphere.vcenter_client import VM
from com.vmware.vcenter.vm.guest_client import OperatingSystem
from vmware.vapi.vsphere.client import create_vsphere_client
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# vSphere credentials and server
VS_HOST = "192.168.0.251"
VS_USER = "administrator@vsphere.local"
VS_PASSWORD = "Time4work!"

# API endpoint for creating a session
URL = f"https://{VS_HOST}/rest/com/vmware/cis/session"


def get_vsphere_client():
    session = requests.session()
    session.verify = False
    client = create_vsphere_client(server=VS_HOST, username=VS_USER, password=VS_PASSWORD, session=session)
    return client


# Function to get the session ID (token)
def get_vsphere_token():
    try:
        # Create a session and authenticate
        response = requests.post(URL, auth=(VS_USER, VS_PASSWORD), verify=False)
        response.raise_for_status()

        # Extract the session ID (token)
        session_id = response.json()['value']
        print(f"Session ID (Token): {session_id}")

        return session_id
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to create a VM
def create_vm(session_id, os):
    try:
        headers = {'vmware-api-session-id': session_id}
        data = {
            "spec": {
                "name": "test-vm-asx",
                "guest_OS": os,  # Correct value for guest_OS as per the documentation
                "placement": {
                    "datastore": "datastore-14",  # Replace with your actual datastore ID
                    "folder": "group-v1010",  # Replace with your actual folder ID
                    "resource_pool": "resgroup-10"  # Replace with your actual resource pool ID
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
                            "network": "palo-to-vm",  # Replace with your actual network ID
                            "start_connected": True
                        }
                    ]
                }
            }
        }

        response = requests.post(
            f"https://{VS_HOST}/rest/vcenter/vm",
            headers=headers,
            json=data,
            verify=False  # Disable SSL verification for simplicity
        )
        response.raise_for_status()
        result = response.json()
        print(f"VM creation result: {json.dumps(result, indent=4)}")
        return True
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
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
            verify=False  # Disable SSL verification for simplicity
        )
        response.raise_for_status()
        folders = response.json()
        print(f"Folders: {json.dumps(folders, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
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
            verify=False  # Disable SSL verification for simplicity
        )
        response.raise_for_status()
        clusters = response.json()
        print(f"Clusters: {json.dumps(clusters, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
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
            verify=False  # Disable SSL verification for simplicity
        )
        response.raise_for_status()
        networks = response.json()
        print(f"Networks: {json.dumps(networks, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
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
            verify=False  # Disable SSL verification for simplicity
        )
        response.raise_for_status()
        datastores = response.json()
        print(f"Datastores: {json.dumps(datastores, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
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
            verify=False  # Disable SSL verification for simplicity
        )
        response.raise_for_status()
        resource_pools = response.json()
        print(f"Resource Pools: {json.dumps(resource_pools, indent=4)}")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to list available guest OS families and OS types
def list_vsphere_guest_os(client):
    try:
        os_families = client.vcenter.VM.Guest.OperatingSystemFamily.list()
        os_types = client.vcenter.VM.Guest.OperatingSystem.list()

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

        client = get_vsphere_client()
        print("\nListing available guest OS families and OS types:")
        list_vsphere_guest_os(client)

        print("\nCreating VM:")
        for os in ["windows7Guest", "rhel7Guest", "centos7Guest", "ubuntu64Guest"]:
            print("OS", os)
            if create_vm(token, os):
                break
