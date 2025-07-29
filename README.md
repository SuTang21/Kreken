# Kreken

This is a python CLI that runs a proxy server intercepting password hash queries to HIBP database and returns a list plaintext mapping of the hashed suffixes HIBP returns. So the qeuried password might be in there somewhere ...

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
<img width="704" height="461" alt="Screenshot 2025-07-29 at 2 01 58 pm" src="https://github.com/user-attachments/assets/2eca57d2-c36f-42cc-a25d-b42a27143026" />

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
<img width="865" height="853" alt="Screenshot 2025-07-29 at 2 24 49 pm" src="https://github.com/user-attachments/assets/24f60cc5-2f65-451f-8c7f-ce30a4d783bb" />

Download certificate according to your system and once downloaded, change the extension of the certificate to '.crt'. 

Open up Keychain Access (Apple) and add certificate under System keychains.
<img width="870" height="519" alt="Screenshot 2025-07-29 at 2 25 58 pm" src="https://github.com/user-attachments/assets/2117451a-d35e-4603-9f65-e265a6aeaaf4" />

Right-click on certificate to open 'Get Info' and under 'Trust', change the 'When using this certificate' value to 'Always Trust'.
<img width="508" height="426" alt="Screenshot 2025-07-29 at 2 27 16 pm" src="https://github.com/user-attachments/assets/925ab5e8-558d-4040-be76-b2492b1d7a07" />

#### 3. Download database

Download database (sorry it's massive - 2.25GB) from here: https://drive.google.com/drive/folders/1NGWSbVX4Iqp4T60o8BAnjiqphBTj9xDD?usp=sharing. Move database into the 'data' folder of the working directory.

#### 4. (Finally) Run Kreken

Ensure HTTP/HTTPS are set to use 127.0.0.1:8080, path is in working directory and python virtual environment is activated.

Run:
```text
python3 proxy.py
```
Which should show something like this:
<img width="993" height="557" alt="Screenshot 2025-07-29 at 2 28 23 pm" src="https://github.com/user-attachments/assets/78a1846a-bfb2-41cd-af0d-9e3f3d71c159" />

To test, open a new terminal and run:
```bash
curl -x https://127.0.0.1:8080 /https:api.pwnedpasswords.range/{first 5 characters of any SHA1}
```

### Structure
- _Proxy.py_ - Set up mitmproxy server and listen to queries to HIBP API.
- _Data.py_ - Process SecList text files into SQLite database.
- _Kreken.py_ - Handles database querying
