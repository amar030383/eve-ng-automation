#!/usr/bin/env python3
"""
manual.py - List all available labs in EVE-NG
"""

import requests
import urllib3
import sys
import logging
from urllib.parse import urljoin

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

EVE_HOST = "192.168.67.150"
EVE_USERNAME = "admin"
EVE_PASSWORD = "eve"
BASE_URL = f"http://{EVE_HOST}"

session = requests.Session()
session.verify = False
session.headers.update({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
})

def login():
    url = urljoin(BASE_URL, "/api/auth/login")
    data = {"username": EVE_USERNAME, "password": EVE_PASSWORD}
    logger.info(f"Logging in to EVE-NG at {EVE_HOST}...")
    resp = session.post(url, json=data)
    if resp.status_code == 200:
        logger.info("Login successful.")
        return True
    else:
        logger.error(f"Login failed: {resp.status_code} - {resp.text}")
        return False

def test_api_endpoints():
    """Test different API endpoints to find the correct one for labs"""
    endpoints = [
        "/api/labs",
        "/api/labs/",
        "/api/labs/status",
        "/api/status",
        "/api/folders",
        "/api/folders/",
        "/api/",
        "/api"
    ]
    
    print("Testing API endpoints:")
    print("=" * 50)
    
    for endpoint in endpoints:
        url = urljoin(BASE_URL, endpoint)
        logger.info(f"Testing endpoint: {endpoint}")
        resp = session.get(url)
        print(f"Endpoint: {endpoint}")
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:200]}...")  # Show first 200 chars
        print("-" * 30)

def list_labs():
    url = urljoin(BASE_URL, "/api/folders/")
    logger.info("Fetching available labs...")
    resp = session.get(url)
    if resp.status_code == 200:
        data = resp.json().get('data', {})
        labs = data.get('labs', [])
        if not labs:
            print("No labs found.")
            return
        print("Available Labs:")
        for lab in labs:
            print(f"- {lab.get('file')} (Path: {lab.get('path')}, Modified: {lab.get('mtime')})")
    else:
        logger.error(f"Failed to fetch labs: {resp.status_code} - {resp.text}")
        print("Failed to fetch labs.")

def main():
    if not login():
        sys.exit(1)
    list_labs()

if __name__ == "__main__":
    main()
