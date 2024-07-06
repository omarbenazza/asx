import requests
import json
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
def create_vm(session_id):
    try:
        headers = {'vmware-api-session-id': session_id}
        data = {
            "spec": {
                "name": "test-vm",
                "guest_OS": "OTHER_64",  # Correct value for guest_OS as per the documentation
                "placement": {
                    "datastore": "datastore-123",  # Replace with your actual datastore ID
                    "folder": "Discovered virtual machine",          # Replace with your actual folder ID
                    "cluster": "domain-c7"         # Replace with your actual cluster ID
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
                            "network": "network-123",  # Replace with your actual network ID
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
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if e.response.content:
            print(f"Error content: {e.response.content.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

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

# Main execution
if __name__ == "__main__":
    token = get_vsphere_token()
    if token:
        print("Listing folders:")
        list_vsphere_folders(token)
        print("\nCreating VM:")
        create_vm(token)
