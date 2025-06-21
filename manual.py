#!/usr/bin/env python3
"""
EVE-NG Manual Lab Management Script
A simple script to interact with EVE-NG labs manually.
"""

import requests
import json
import sys
from typing import Dict, List, Optional
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EVENGLabManager:
    def __init__(self, host: str, username: str, password: str, port: int = 80):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        self.session.verify = False
        
    def login(self) -> bool:
        """Login to EVE-NG and get session cookie"""
        try:
            login_url = f"{self.base_url}/api/auth/login"
            login_data = {
                "username": self.username,
                "password": self.password
            }
            
            response = self.session.post(login_url, json=login_data)
            
            if response.status_code == 200:
                print(f"✅ Successfully logged in to EVE-NG at {self.host}")
                return True
            else:
                print(f"❌ Login failed. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def list_labs(self) -> List[Dict]:
        """List all available labs"""
        try:
            # Try the correct endpoint for listing labs
            labs_url = f"{self.base_url}/api/folders/"
            
            response = self.session.get(labs_url)
            
            if response.status_code == 200:
                labs_data = response.json()
                labs = []
                
                # Parse the labs from the response
                if 'data' in labs_data:
                    for item in labs_data['data']:
                        if item.get('type') == 'lab':
                            labs.append({
                                'name': item.get('name', 'Unknown'),
                                'path': item.get('path', ''),
                                'description': item.get('description', ''),
                                'author': item.get('author', ''),
                                'version': item.get('version', ''),
                                'body': item.get('body', '')
                            })
                
                return labs
            else:
                print(f"❌ Failed to fetch labs. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error listing labs: {e}")
            return []
    
    def get_lab_info(self, lab_name: str) -> Optional[Dict]:
        """Get detailed information about a specific lab"""
        try:
            lab_url = f"{self.base_url}/api/labs/{lab_name}/"
            
            response = self.session.get(lab_url)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get lab info for {lab_name}. Status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting lab info: {e}")
            return None

def main():
    """Main function to run the lab manager"""
    print("🔧 EVE-NG Manual Lab Manager")
    print("=" * 40)
    
    # Configuration - Update these values
    EVE_HOST = "192.168.1.100"  # Your EVE-NG server IP
    EVE_USERNAME = "admin"      # Your EVE-NG username
    EVE_PASSWORD = "eve"        # Your EVE-NG password
    EVE_PORT = 80              # EVE-NG web interface port
    
    # Create lab manager instance
    lab_manager = EVENGLabManager(EVE_HOST, EVE_USERNAME, EVE_PASSWORD, EVE_PORT)
    
    # Login
    if not lab_manager.login():
        print("❌ Cannot proceed without successful login")
        sys.exit(1)
    
    # List labs
    print("\n📋 Available Labs:")
    print("-" * 40)
    
    labs = lab_manager.list_labs()
    
    if labs:
        for i, lab in enumerate(labs, 1):
            print(f"{i}. {lab['name']}")
            if lab.get('description'):
                print(f"   Description: {lab['description']}")
            if lab.get('author'):
                print(f"   Author: {lab['author']}")
            if lab.get('version'):
                print(f"   Version: {lab['version']}")
            print()
    else:
        print("No labs found or error occurred while fetching labs.")
    
    print(f"Total labs found: {len(labs)}")

if __name__ == "__main__":
    main() 