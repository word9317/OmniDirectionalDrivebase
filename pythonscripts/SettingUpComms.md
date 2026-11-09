# ROCK 4C+ Headless Communications Bridge
Comms server on the Rock 4 C+ Tutorial
# 1. Install OS
I used Debian since Radxa doesnt make any other Operating systems for the Rock 4 C+. I recommend using Debian as this document is talored for it.
# 2. Update Debian

```bash
sudo apt update
sudo apt upgrade -y
```

Install required packages:
```bash
sudo apt install \
hostapd \
dnsmasq \
openssh-server \
python3 \
python3-pip \
python3-serial \
dos2unix
```
# 3. Determine Your Username(kinda useful, idk)
Run:
```bash
whoami
```
Replace `user` everywhere in this guide with what you just found
# 4. Enable SSH

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

Verify:

```bash
systemctl status ssh
```

Should show:

```text
active (running)
```
# 5. Configure Automatic Login

Create:

```bash
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
```

Create:

```bash
sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf
```

Paste:

```ini
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin user --noclear %I $TERM
```





Reload:

```bash
sudo systemctl daemon-reload
```



# 6. Configure Passwordless Sudo

Run:

```bash
sudo visudo
```

Add:

```text
user ALL=(ALL) NOPASSWD: ALL
```

Save and exit.



# 7. Configure Hotspot

Create:

```bash
sudo nano /etc/hostapd/hostapd.conf
```

Paste:

```ini
interface=wlan0
driver=nl80211

ssid=NameYourRobot

hw_mode=g
channel=6

wmm_enabled=0
auth_algs=1

wpa=2
wpa_passphrase=superSecurePassword

wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
```
MAKE SURE YOU USE HYPHEN, I WASTED LIKE 10 MINUTES TRYING TO FIX IT
# 8. Point hostapd at the Config

Edit:

```bash
sudo nano /etc/default/hostapd
```

Set:

```ini
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```



# 9. Configure DHCP

Edit:

```bash
sudo nano /etc/dnsmasq.conf
```

Add to the bottom:

```ini
interface=wlan0
dhcp-range=192.168.4.10,192.168.4.50,255.255.255.0,24h
```



# 10. Disable Wi-Fi Managers

These commonly break hotspot mode.

```bash
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager

sudo systemctl stop wpa_supplicant
sudo systemctl disable wpa_supplicant
```



# 11. Enable Services

```bash
sudo systemctl unmask hostapd

sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```



# 12. Make 192.168.4.1 Persistent

Create:

```bash
nano ~/setup_hotspot.sh
```

Paste:

```bash
#!/bin/bash

ip addr flush dev wlan0
ip addr add 192.168.4.1/24 dev wlan0
ip link set wlan0 up

systemctl restart hostapd
systemctl restart dnsmasq
```

Make executable:

```bash
chmod +x ~/setup_hotspot.sh
```



Create service:

```bash
sudo nano /etc/systemd/system/hotspot-init.service
```

Paste:

```ini
[Unit]
Description=Assign Hotspot IP
After=network.target

[Service]
Type=oneshot

ExecStart=/home/user/setup_hotspot.sh

[Install]
WantedBy=multi-user.target
```





Enable:

```bash
sudo systemctl daemon-reload

sudo systemctl enable hotspot-init
```

# 13. Start Hotspot

```bash
sudo systemctl start hostapd
sudo systemctl start dnsmasq
```

Verify:

```bash
systemctl status hostapd
systemctl status dnsmasq
```

Both should show:

```text
active (running)
```



# 14. Verify from Windows

Connect to:

```text
NameYourRobot
```

Password:

```text
superSecurePassword
```

Run:

```cmd
ipconfig
```

Expected:

```text
IPv4 Address : 192.168.4.x
Default Gateway : 192.168.4.1
```

Bad:

```text
169.254.x.x
```

If you see that, DHCP is not working.



# 15. Verify Connectivity

On Windows:

```cmd
ping 192.168.4.1
```

You should get replies.



# 16. SSH Into the ROCK

From PowerShell:

```powershell
ssh user@192.168.4.1
```
# 17. Create Communication Server

Create:(FIND IN THIS DIRECTORY AS 'main.py')

```bash
nano ~/main.py
```

Paste your communications server.

Test manually:

```bash
python3 ~/main.py
```

Expected:

```text
Connected to Arduino
Listening on 0.0.0.0:5000
```

Stop with:

```text
Ctrl+C
```



# 18. Verify Python Dependencies

Run:

```bash
python3
```

Then:

```python
import serial
```

No errors should appear.

Exit:

```python
exit()
```



# 19. Prepare Script For Systemd

Make executable:

```bash
chmod +x ~/comms_server.py
```

Remove Windows line endings:

```bash
dos2unix ~/comms_server.py
```

This prevents:

```text
203/EXEC
```

errors.



# 20. Create Communication Service

Create:

```bash
sudo nano /etc/systemd/system/comms.service
```

Paste:

```ini
[Unit]
Description=ROCK Communications Server
After=network-online.target

[Service]
Type=simple

User=user
WorkingDirectory=/home/user

ExecStart=/usr/bin/python3 /home/user/comms_server.py

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```







# 21. Verify Service Before Enabling

Run:

```bash
sudo systemd-analyze verify /etc/systemd/system/comms.service
```

Expected:

```text
(no output)
```

If errors appear, fix them before continuing.


# 22. Enable Communication Service

```bash
sudo systemctl daemon-reload

sudo systemctl enable comms

sudo systemctl start comms
```



# 23. Verify Service

```bash
sudo systemctl status comms
```

Expected:

```text
active (running)
```



# 24. View Logs

```bash
sudo journalctl -u comms -f
```



# 25. Verify Listening Port

```bash
sudo ss -tlnp | grep 5000
```

Expected:

```text
LISTEN 0 1 0.0.0.0:5000
```



# 26. Laptop Client Settings

Use:

```python
ROCK_IP = "192.168.4.1"
PORT = 5000
```