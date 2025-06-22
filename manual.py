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
  {
      "template": "iol",
      "type": "iol",
      "count": "1",
      "image": "i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin",
      "name": "R",
      "icon": "Router.png",
      "nvram": "1024",
      "ram": "1024",
      "ethernet": "1",
      "serial": "0",
      "config": "0",
      "delay": "0",
      "left": "210",
      "top": "249",
      "postfix": 0
  }
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

def createNodes():
    for data in template:
        create_node_url = f"{BASE_URL}/api/labs/4_VLAN_Automation_single_Portchannel.unl/nodes"
        payload = json.dumps(data)
        create_node = session.post(url = create_node_url, data=payload)
        print(create_node.status_code)

def main():
    if login():
        print("\n🔍 Available labs:")
        list_labs()
        print(f"\n🎯 Target lab: {lab_config.get('target_lab', 'Enterprise_Automated_Lab.unl')}")
        createNodes()        

if __name__ == "__main__":
    main() 