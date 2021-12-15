## Open VPN Speed Test 

### Python libraries
- [pip3 install tqdm](https://tqdm.github.io/)
- [pip3 install paramiko](https://www.paramiko.org/)
- [pip3 install scp](https://pypi.org/project/scp/)

### 1. Set up Server device.  
- Static WAN IP address (e.g. 10.0.0.30, netmask 255.255.255.0)
- Static LAN IP address (e.g. 192.168.3.1, netmask 255.255.255.0)

### 2. Set up Client device.
- Static WAN IP address (e.g. 10.0.0.20, netmask 255.255.255.0)
- Static LAN IP address (e.g. 192.168.2.1, netmask 255.255.255.0)
- Enable traffic rule - Enable_SSH_WAN  
![alt text](https://github.com/zyygis/OpenVPN_speed_test/blob/master/traffic%20rule.png)

### 3. Connect devices with Ethernet cable via WAN port.

### Wired WAN Topology
![alt text](https://github.com/zyygis/OpenVPN_speed_test/blob/master/diagram.png)
### Mobile Topology
![alt text]()
### 4. In info.json file fill in necessary information.

- Speed test through **WIRED WAN**. In info.json file in "Server_WAN_ip" line enter **WAN IP ADDRESS** (Server_WAN_ip": "**WAN IP**").
- Speed test through **MOBILE**. In info.json file in "Server_WAN_ip" line enter **MOBILE PUBLIC IP ADDRESS** (Server_WAN_ip": "**MOBILE PUBLIC IP**").  
  
Example below is Speed test through **WIRED WAN**.
```json
{
  "client_config": 
  {
    "Config_name": "router2",
    "Server_LAN_ip": "192.168.3.1",
    "Server_WAN_ip": "10.0.0.30",
    "Server_User": "root",
    "Server_Password": "Admin123",
    "Encryption":"DESX-CBC",
    "LZO":"yes",
    "Protocol":"tcp-client",
    "Authentication":"static key"
  },
  "server_config":
  {
    "Config_name": "router1",
    "Client_LAN_ip": "192.168.2.1",
    "Client_WAN_ip": "10.0.0.20",
    "Client_User": "root",
    "Client_Password": "Admin123",
    "Encryption":"DESX-CBC",
    "LZO":"yes",
    "Protocol":"tcp-server",
    "Authentication":"static key"
  }
}
```

**Encryption types:**  
- DES-CBC  
- DES-EDE-CBC  
- DES-EDE3-CBC  
- DESX-CBC  
- BF-CBC  
- CAST5-CBC  
- AES-128-CBC  
- AES-192-CBC  
  
**Protocol:**  
- udp
- tpc-server (for server device)
- tpc-client (for client device)  

**Authentication mode available is only static key.**  

### 5. Command line arguments  
- -t, --testcycles | Number for how many iperf3 test to run. (Default is 5)
- -f, --filename | Test report file name. (Default is OpenVPN_report)

Test report is saved in ~/OpenVPN_test/Test_report  

### Start the Test
Navigate to ~/OpenVPN_speed_test folder.  
In the terminal enter: python3 main.py

### Example of Test Report
![alt text](https://github.com/zyygis/OpenVPN_speed_test/blob/master/test_report.png)
