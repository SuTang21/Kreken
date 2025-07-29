# Kreken

This is a python CLI that runs a proxy server intercepting password hashes 

### Installation
_For MacOS_

#### 1. Python virtual environment

Create virtual environment in desired folder.
```bash
python -m venv <path to virtual environment>
```

Activate environment.
```bash
cd <path to virtual environment>
source bin/activate
```
#### 2. Run mitmproxy
```bash
pip install mitmproxy
```
Proxy runs locally on port 8080, to configure go to: Settings > Network > WiFi Details > Proxies and turn on Web proxy (HTTP) and Secure web proxy (HTTPs). Configure both to have the following settings:
```text
Sever: 127.0.0.1
Port: 8080
```
Or use run command in terminal:
```bash
INTERFACE="Wi-Fi"                   
PROXY_ADDRESS="127.0.0.1"
PROXY_PORT="8080"

# Enable Web Proxy (HTTP)
networksetup -setwebproxy "$INTERFACE" "$PROXY_ADDRESS" "$PROXY_PORT"
networksetup -setwebproxystate "$INTERFACE" on

# Enable Secure Web Proxy (HTTPS)
networksetup -setsecurewebproxy "$INTERFACE" "$PROXY_ADDRESS" "$PROXY_PORT"
networksetup -setsecurewebproxystate "$INTERFACE" on
```

Command to turn off proxy:
```bash
INTERFACE="Wi-Fi"                   

# Turn off Web Proxy (HTTP)
networksetup -setwebproxystate "$INTERFACE" off

# Turn off Secure Web Proxy (HTTPS)
networksetup -setsecurewebproxystate "$INTERFACE" off
```

To test `mitmproxy` is installed properly, run the following command in same python virtual environment started earlier.
```bash
mitmproxy
```
While proxy is running, visit 'http://mitm.it' in browser. If proxy is configured properly, this should show up:

Download certificate according to your system and once downloaded, change the extension of the certificate to '.crt'. 

Open up Keychain Access (Apple) and add certificate under System keychains.

Right-click on certificate to open 'Get Info' and under 'Trust', change the 'When using this certificate' value to 'Always Trust'.

#### 2. Run mitmproxy

Install `mitmproxy` (https://mitmproxy.org/) into python virtual environment folder.

#### Details
