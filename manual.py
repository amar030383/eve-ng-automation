import requests
import json
import os

template = [
  {
      "template": "asav",
      "type": "qemu",
      "count": "1",
      "image": "asav-941-200",
      "name": "ASAv",
      "icon": "ASA.png",
      "uuid": "",
      "cpulimit": "",
      "cpu": "1",
      "ram": "2048",
      "ethernet": "8",
      "qemu_version": "",
      "qemu_arch": "",
      "qemu_nic": "",
      "qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -cpu host -nodefaults -display none -vga std -rtc base=utc",
      "ro_qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -cpu host -nodefaults -display none -vga std -rtc base=utc",
      "config": "0",
      "delay": "0",
      "console": "telnet",
      "left": "1091",
      "top": "118",
      "postfix": 0
  },
#   {
#       "template": "iol",
#       "type": "iol",
#       "count": "1",
#       "image": "i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin",
#       "name": "R",
#       "icon": "Router.png",
#       "nvram": "1024",
#       "ram": "1024",
#       "ethernet": "1",
#       "serial": "0",
#       "config": "0",
#       "delay": "0",
#       "left": "210",
#       "top": "249",
#       "postfix": 0
#   },
#   {"template":"c1710","type":"dynamips","count":"1","image":"c1710-bk9no3r2sy-mz.124-23.image","name":"1710","icon":"Router2.png","idlepc":"0x80369ac4","nvram":"128","ram":"96","config":"0","delay":"0","left":"1048","top":"489","postfix":0},
#   {"template":"c3725","type":"dynamips","count":"1","image":"c3725-adventerprisek9-mz.124-15.T14.image","name":"3725","icon":"Router.png","idlepc":"0x60c08728","nvram":"128","ram":"256","slot1":"NM-1FE-TX","slot2":"NM-16ESW","config":"0","delay":"0","left":"202","top":"435","postfix":0},
#   {"template":"c7200","type":"dynamips","count":"1","image":"c7200-adventerprisek9-mz.152-4.S7.image","name":"7206VXR","icon":"Router.png","idlepc":"0x62f21000","nvram":"128","ram":"256","slot1":"PA-4E","slot2":"PA-4E","slot3":"","slot4":"","slot5":"","slot6":"","config":"0","delay":"0","left":"333","top":"510","postfix":0},
#   {"template":"nxosv9k","type":"qemu","count":"1","image":"nxosv9k-7.0.3.I7.4","name":"NXOS","icon":"Nexus7K.png","uuid":"","cpulimit":"undefined","cpu":"2","ram":"8192","ethernet":"8","qemu_version":"","qemu_arch":"","qemu_nic":"","qemu_options":"-machine type=pc,accel=kvm -serial mon:stdio -nographic -enable-kvm -cpu host","ro_qemu_options":"-machine type=pc,accel=kvm -serial mon:stdio -nographic -enable-kvm -cpu host","config":"0","delay":"0","console":"telnet","left":"208","top":"400","postfix":0},
#   {"template":"viosl2","type":"qemu","count":"1","image":"viosl2-adventerprisek9-m.SSA.high_iron_20200929","name":"Switch","icon":"Switch.png","uuid":"","cpulimit":"undefined","cpu":"1","ram":"1024","ethernet":"8","qemu_version":"","qemu_arch":"","qemu_nic":"","qemu_options":"-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -nodefaults -rtc base=utc -cpu host","ro_qemu_options":"-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -nodefaults -rtc base=utc -cpu host","config":"0","delay":"0","console":"telnet","left":"251","top":"466","postfix":0},
#   {"template":"vpcs","type":"vpcs","count":"1","name":"VPC","icon":"Laptop.png","config":"0","delay":"0","left":"264","top":"332","postfix":0},
]


def load_config():
    """Load configuration from config.json file"""
    config_file = "config.json"
    if not os.path.exists(config_file):
        print(f"❌ Config file {config_file} not found!")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

# Load configuration
config = load_config()
if not config:
    exit(1)


# Extract configuration values
eve_config = config['eve_ng']
api_endpoints = config['api_endpoints']
lab_config = config['lab']

protocol = "https" if eve_config.get('use_ssl', False) else "http"
BASE_URL = f"{protocol}://{eve_config['host']}"

session = requests.Session()
session.verify = False

def login():
    url = f"{BASE_URL}{api_endpoints['login']}"
    data = {"username": eve_config['username'], "password": eve_config['password']}
    resp = session.post(url, json=data)
    if resp.status_code == 200:
        print(f"✅ Logged in to EVE-NG at {eve_config['host']}")
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

def createNodes(labname):
    node_id = []
    print(f"Creating nodes for {labname}")
    for data in template:
        create_node_url = f"{BASE_URL}/api/labs/{labname}/nodes"
        payload = json.dumps(data)
        create_node = session.post(url = create_node_url, data=payload)
        if create_node.status_code == 201:
            node_id.append(create_node.json().get('data').get('id'))
            print(f"Node {data.get('name')} created successfully")
        else:
            print(f"Node creation failed: {create_node.status_code} {create_node.text}")
    return node_id

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
        ids = createNodes(labname) 
        print(ids)
        if input("Do you want to start the nodes? (y/n)") == 'y':
            startNodes(ids, labname)
        else:
            print("Nodes not started")
        print("--------------------------------")
        if input("Do you want to stop the nodes? (y/n)") == 'y':
            stopNodes(ids, labname)
        else:
            print("Nodes not stopped")
        
        if input("Do you want to delete the nodes? (y/n)") == 'y':
            deleteNodes(ids, labname)
        else:
            print("Nodes not deleted")

if __name__ == "__main__":
    main() 