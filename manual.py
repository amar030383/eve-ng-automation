#!/usr/bin/env python3
"""
Minimal EVE-NG Lab Listing Script
Logs in to EVE-NG and lists available labs.
"""

import requests
import urllib3
import json
import os

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# Set up base URL
protocol = "https" if eve_config.get('use_ssl', False) else "http"
BASE_URL = f"{protocol}://{eve_config['host']}:{eve_config['port']}"

session = requests.Session()
session.verify = False

def login():
    url = f"{BASE_URL}{api_endpoints['login']}"
    data = {"username": eve_config['username'], "password": eve_config['password']}
    resp = session.post(url, json=data)
    if resp.status_code == 200:
        # print(f"✅ Logged in to EVE-NG at {eve_config['host']}")
        return True
    print(f"❌ Login failed: {resp.status_code} {resp.text}")
    return False

def list_labs():
    url = f"{BASE_URL}{api_endpoints['folders']}"
    resp = session.get(url)
    # print(f"[DEBUG] /api/folders/ response: {resp.text}")
    if resp.status_code == 200:
        try:
            data = resp.json()
            # The labs are in data.data.labs, not data.data
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

def find_lab_path(lab_name):
    url = f"{BASE_URL}{api_endpoints['folders']}"
    resp = session.get(url)
    if resp.status_code == 200:
        try:
            data = resp.json()
            # The labs are in data.data.labs, not data.data
            labs_data = data.get('data', {}).get('labs', [])
            
            for lab in labs_data:
                if lab.get('file') == lab_name:
                    # print(f"Found lab '{lab_name}' at path: {lab.get('path')}")
                    return lab.get('path')
            print(f"Lab '{lab_name}' not found.")
        except Exception as e:
            print(f"❌ Error parsing labs: {e}")
    else:
        print(f"❌ Failed to get labs: {resp.status_code} {resp.text}")
    return None

def get_node_types():
    """Get available node types from EVE-NG"""
    url = f"{BASE_URL}{api_endpoints['templates']}"
    resp = session.get(url)
    print(f"[DEBUG] Node types response: {resp.status_code} {resp.text}")
    if resp.status_code == 200:
        try:
            data = resp.json()
            print("\nAvailable Node Types:")
            for node_type in data:
                print(f"  - {node_type}")
            return data
        except Exception as e:
            print(f"❌ Error parsing node types: {e}")
    else:
        print(f"❌ Failed to get node types: {resp.status_code} {resp.text}")
    return []

def get_templates(node_type):
    """Get available templates for a specific node type"""
    url = f"{BASE_URL}/api/list/templates/{node_type}"
    resp = session.get(url)
    print(f"[DEBUG] Templates for {node_type} response: {resp.status_code} {resp.text}")
    if resp.status_code == 200:
        try:
            data = resp.json()
            print(f"\nAvailable Templates for {node_type}:")
            for template in data:
                print(f"  - {template}")
            return data
        except Exception as e:
            print(f"❌ Error parsing templates: {e}")
    else:
        print(f"❌ Failed to get templates for {node_type}: {resp.status_code} {resp.text}")
    return []

def create_node(lab_path, node_name="TestNode1", node_type="qemu", template="vios", x=100, y=100):
    url = f"{BASE_URL}/api/labs{lab_path}/nodes"
    payload = {
        "name": node_name,
        "type": node_type,
        "template": template,
        "icon": "Router.png",
        "x": x,
        "y": y
    }
    resp = session.post(url, json=payload)
    print(f"[DEBUG] Create node response: {resp.status_code} {resp.text}")
    if resp.status_code == 201:
        print(f"✅ Node '{node_name}' created successfully in lab {lab_path}")
    else:
        print(f"❌ Failed to create node: {resp.status_code} {resp.text}")

def try_templates_endpoints():
    """Try different template endpoints to find the correct one"""
    ep = api_endpoints['templates']
    available_templates = []
    
    url = f"{BASE_URL}{ep}"
    resp = session.get(url)

    if resp.status_code == 200:
        try:
            data = resp.json()
            if isinstance(data, dict):
                # Filter templates that have images
                for template_type, templates in data.items():
                    if isinstance(templates, list) and templates:
                        # Check if templates have actual images
                        available = []
                        for template in templates:
                            if isinstance(template, dict):
                                # Check if template has image information
                                if template.get('image') or template.get('path') or template.get('available'):
                                    available.append(template)
                            elif isinstance(template, str) and template.strip():
                                # Simple string template
                                available.append(template)
                        
                        if available:
                            print(f"  ✅ {template_type}: {len(available)} available templates")
                            for template in available:
                                if isinstance(template, dict):
                                    name = template.get('name', template.get('image', 'Unknown'))
                                    print(f"    - {name}")
                                else:
                                    print(f"    - {template}")
                            available_templates.extend(available)
                        else:
                            print(f"  ❌ {template_type}: No images available")
                    else:
                        print(f"  ❌ {template_type}: No templates found")
                        
        except Exception as e:
            print(f"❌ Error parsing templates from {ep}: {e}")
    else:
        print(f"❌ Failed to get templates from {ep}: {resp.status_code} {resp.text}")

    # print(f"\n📋 Summary: Found {len(available_templates)} total available templates")
    return available_templates

def main():
    if login():
        list_labs()
        lab_path = find_lab_path(lab_config['target_lab'])
        if lab_path:
            # print(f"Lab path for node creation: {lab_path}")
            available_templates = try_templates_endpoints()
            
            if available_templates:
                print(available_templates)
                # Use the first available template to create a node
                # first_template = available_templates[0]
                # if isinstance(first_template, dict):
                #     template_name = first_template.get('name', first_template.get('image', 'Unknown'))
                #     template_type = first_template.get('type', 'qemu')
                # else:
                #     template_name = str(first_template)
                #     template_type = 'qemu'
                
                # print(f"\n🔧 Creating node with template: {template_name}")
                # create_node(lab_path, node_name="TestNode1", node_type=template_type, template=template_name)
            else:
                print("❌ No available templates found for node creation")
        
if __name__ == "__main__":
    main() 