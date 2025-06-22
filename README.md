# EVE-NG Lab Automation Script (`manual.py`)

A Python automation script for EVE-NG that provides lab management capabilities including authentication, lab listing, and automated node creation using predefined templates.

## Features

- **Secure Authentication**: Connects to EVE-NG using REST API with configurable SSL support
- **Lab Management**: Lists all available labs with detailed information
- **Node Creation**: Automatically creates network devices (ASAv, IOL routers) using predefined templates
- **Configuration Management**: External configuration file support for easy customization
- **Template System**: Pre-configured device templates for common network equipment

## Prerequisites

- Python 3.x
- EVE-NG server running and accessible
- Network access to your EVE-NG instance

## Installation

1. **Clone or download the project files**
2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The script uses `config.json` for all configuration settings. Edit this file to match your EVE-NG setup:

### EVE-NG Server Configuration
```json
{
  "eve_ng": {
    "host": "192.168.67.150",
    "username": "admin", 
    "password": "eve",
    "port": 80,
    "use_ssl": false,
    "timeout": 30
  }
}
```

### API Endpoints
The configuration includes comprehensive API endpoints for various EVE-NG operations:
- Authentication endpoints
- Lab management endpoints  
- Node management endpoints
- Network and topology endpoints

### Lab Configuration
```json
{
  "lab": {
    "target_lab": "Enterprise_Automated_Lab.unl"
  }
}
```

## Usage

### Basic Usage
```bash
python manual.py
```

### What the script does:
1. **Loads configuration** from `config.json`
2. **Authenticates** with your EVE-NG server
3. **Lists available labs** showing file names and paths
4. **Creates nodes** in the target lab using predefined templates

### Current Templates

The script includes two device templates:

#### ASAv (Adaptive Security Appliance Virtual)
- **Type**: QEMU virtual machine
- **Image**: asav-941-200
- **Resources**: 1 CPU, 2GB RAM, 8 Ethernet interfaces
- **Console**: Telnet
- **QEMU Options**: Optimized for KVM acceleration

#### IOL Router (IOS on Linux)
- **Type**: IOL container
- **Image**: i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
- **Resources**: 1GB RAM, 1GB NVRAM, 1 Ethernet interface
- **Console**: Serial

## Output Example

```
✅ Logged in to EVE-NG at 192.168.67.150

🔍 Available labs:
1. 4_VLAN_Automation_single_Portchannel.unl (Path: /4_VLAN_Automation_single_Portchannel.unl)
2. Enterprise_Automated_Lab.unl (Path: /Enterprise_Automated_Lab.unl)
3. Auctopus_lab.unl (Path: /Auctopus_lab.unl)

🎯 Target lab: Enterprise_Automated_Lab.unl
```

## Customization

### Adding New Device Templates
You can extend the `template` list in `manual.py` to add new device types:

```python
{
    "template": "your_template_name",
    "type": "qemu|iol|docker",
    "count": "1",
    "image": "your_image_name",
    "name": "Device Name",
    "icon": "Icon.png",
    "cpu": "1",
    "ram": "1024",
    "ethernet": "4",
    # ... other configuration options
}
```

### Modifying Target Lab
Change the target lab in `config.json`:
```json
{
  "lab": {
    "target_lab": "Your_Lab_Name.unl"
  }
}
```

## Troubleshooting

### Common Issues

1. **Login Failed**
   - Verify EVE-NG host, username, and password in `config.json`
   - Check if EVE-NG server is running and accessible
   - Ensure correct port and SSL settings

2. **Config File Not Found**
   - Make sure `config.json` exists in the same directory as `manual.py`
   - Verify JSON syntax is valid

3. **No Labs Found**
   - Check if you have permission to view labs
   - Verify EVE-NG server has labs created
   - Ensure API endpoints are correct

4. **Node Creation Errors**
   - Verify target lab exists and is accessible
   - Check if required images are available on EVE-NG server
   - Ensure sufficient resources for node creation

### SSL Certificate Issues
If using HTTPS with self-signed certificates, the script disables SSL verification. For production environments, consider proper certificate management.

## Security Considerations

- Store sensitive credentials securely
- Use HTTPS in production environments
- Regularly update passwords and access controls
- Consider using environment variables for credentials

## API Reference

The script uses EVE-NG's REST API endpoints for:
- Authentication (`/api/auth/login`)
- Lab listing (`/api/folders/`)
- Node creation (`/api/labs/{lab_path}/nodes`)
- Node management (start, stop, wipe, etc.)

## Dependencies

- `requests==2.31.0`: HTTP library for API calls
- `urllib3==2.0.7`: HTTP client library
- `cryptography==41.0.7`: Cryptographic recipes and primitives

## License

This script is provided as-is for educational and automation purposes. Use responsibly and in accordance with your EVE-NG license terms.

## Contributing

Feel free to extend the functionality by:
- Adding new device templates
- Implementing additional API endpoints
- Improving error handling and logging
- Adding configuration validation
