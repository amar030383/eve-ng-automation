import requests
import json
from templates import *

host= "192.168.67.150"
username= "admin"
password= "eve"

BASE_URL = f"http://{host}"

session = requests.Session()
session.verify = False

def login():
    url = f"{BASE_URL}/api/auth/login"
    data = {"username": username, "password": password}
    resp = session.post(url, json=data)
    if resp.status_code == 200:
        print(f"✅ Logged in to EVE-NG at {host}")
        return True
    print(f"❌ Login failed: {resp.status_code} {resp.text}")
    return False

def list_labs():
    url = f"{BASE_URL}{api_endpoints['folders']}"
    resp = session.get(url)
    if resp.status_code == 200:
        try:
            data = resp.json()
            labs_data = data.get('data', {}).get('labs', [])
            if not labs_data:
                print("No labs found.")
            else:
                print("\nLabs:")
                for i, lab in enumerate(labs_data, 1):
                    print(f"{i}. {lab.get('file', 'Unknown')} (Path: {lab.get('path', '')})")
        except Exception as e:
            print(f"❌ Error parsing labs: {e}")
            print(f"Raw response: {resp.text}")
    else:
        print(f"❌ Failed to get labs: {resp.status_code} {resp.text}")

def createNodes(template, labname):
    print(f"Creating nodes for {labname}")
    create_node_url = f"{BASE_URL}/api/labs/{labname}/nodes"
    payload = json.dumps(template)
    create_node = session.post(url = create_node_url, data=payload)
    if create_node.status_code == 201:
        print(f"Node {template.get('name')} created successfully")
        return create_node.json().get('data').get('id')
    else:
        print(f"Node creation failed: {create_node.status_code} {create_node.text}")
        return []

def deleteNodes(ids, labname):   
    print(f"Deleting nodes {ids}")
    for id in ids:
        delete_node_url = f"{BASE_URL}/api/labs/{labname}/nodes/{id}"
        delete_node = session.delete(url = delete_node_url)
        if delete_node.status_code == 200:
            print(f"Node {id} deleted successfully")
        else:
            print(f"Node {id} deletion failed")

def startNodes(ids, labname):
    """Start specific nodes by their IDs"""
    print(f"Starting nodes {ids}")
    for node_id in ids:
        start_node_url = f"{BASE_URL}/api/labs/{labname}/nodes/{node_id}/start"
        print(start_node_url)
        start_node = session.get(url=start_node_url)
        if start_node.status_code == 200:
            print(f"✅ Node {node_id} started successfully")
        else:
            print(f"❌ Failed to start node {node_id}: {start_node.status_code} {start_node.text}")

def stopNodes(ids, labname):
    """Stop specific nodes by their IDs"""
    print(f"Stopping nodes {ids}")
    for node_id in ids:
        stop_node_url = f"{BASE_URL}/api/labs/{labname}/nodes/{node_id}/stop"
        stop_node = session.get(url=stop_node_url)
        if stop_node.status_code == 200:
            print(f"✅ Node {node_id} stopped successfully")
        else:
            print(f"❌ Failed to stop node {node_id}: {stop_node.status_code} {stop_node.text}")


def main():
    if login():

        # list_labs()
        labname =  '4_VLAN_Automation_single_Portchannel.unl'
        # for template in c7200,nxosv9k:
        template = c7200
        ids = createNodes(template, labname) 
        print(ids)
        
        # print(ids)
        # print("--------------------------------")
        # if input("Do you want to start the nodes? (y/n)") == 'y':
        #     startNodes(ids, labname)
        # else:
        #     print("Nodes not started")

        # print("--------------------------------")
        # if input("Do you want to stop the nodes? (y/n)") == 'y':
        #     stopNodes(ids, labname)
        # else:
        #     print("Nodes not stopped")
        # print("--------------------------------")
        # if input("Do you want to delete the nodes? (y/n)") == 'y':
        #     deleteNodes(ids, labname)
        # else:
        #     print("Nodes not deleted")

if __name__ == "__main__":
    main() 