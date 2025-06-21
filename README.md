# EVE-NG Lab Listing Script (`manual.py`)

This script allows you to connect to your EVE-NG server and list all available labs using the EVE-NG API.

## Features
- Connects to EVE-NG using the REST API
- Authenticates with your EVE-NG credentials
- Lists all available labs with file name, path, and last modified time
- Simple and easy to use

## Requirements
- Python 3.x
- `requests` and `urllib3` libraries (install with `pip install requests urllib3`)

## Usage

1. **Configure your EVE-NG server details**
   
   Edit the following variables at the top of `manual.py` if needed:
   ```python
   EVE_HOST = "192.168.67.150"
   EVE_USERNAME = "admin"
   EVE_PASSWORD = "eve"
   ```

2. **Run the script**
   ```bash
   python manual.py
   ```

3. **Output**
   The script will display a list of all labs found on your EVE-NG server, for example:
   ```
   Available Labs:
   - 4_VLAN_Automation_single_Portchannel.unl (Path: /4_VLAN_Automation_single_Portchannel.unl, Modified: 30 May 2025 09:12)
   - Auctopus_lab.unl (Path: /Auctopus_lab.unl, Modified: 25 Feb 2024 11:27)
   - Enterprise_Automated_Lab_1750522980.unl (Path: /Enterprise_Automated_Lab_1750522980.unl, Modified: 21 Jun 2025 18:23)
   ...
   ```

## Troubleshooting
- If you see a login error, check your EVE-NG IP, username, and password.
- If you see "No labs found.", your EVE-NG server may not have any labs or you may not have permission to view them.
- If you see a connection error, make sure your EVE-NG server is running and accessible from your machine.

## Customization
- You can further extend the script to filter labs, show more details, or perform actions on labs (open, delete, etc.).

## License
This script is provided as-is for educational and automation purposes. 