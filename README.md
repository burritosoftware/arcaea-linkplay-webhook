# Arcaea Linkplay Webhook
![Icons](https://skillicons.dev/icons?i=py,linux,discord)

[![WakaTime](https://wakatime.com/badge/github/burritosoftware/arcaea-linkplay-webhook.svg)](https://wakatime.com/badge/github/burritosoftware/arcaea-linkplay-webhook)

---

## How this works
This script reads the logs for [Arcaea-server](https://github.com/Lost-MSth/Arcaea-server)'s Link Play server, running in a systemd unit.
It parses log messages for new rooms and sends a nicely-formatted message in Discord, announcing them and any players that join.

![Preview](https://taidums.are-really.cool/5zReRDx.png)

## Limitations
Unfortunately, [Arcaea-server](https://github.com/Lost-MSth/Arcaea-server)'s Link Play server does not print log messages when the host of a room changes, or when players leave/the room is closed. Therefore, the messages sent by this webhook won't be edited if a player leaves or the room is closed.

## Installation
1. Make sure that you're running the Link Play server seperately. [Follow this guide](https://github.com/Lost-MSth/Arcaea-server/wiki/Instruction-for-use#run-a-stand-alone-link-play-server) to configure that.
2. Create a systemd service to run the Link Play server under.  
   For example, in a file named `arcaea-linkplay.service` at `/etc/systemd/system`:
   ```ini
   [Unit]
   Description=Arcaea Link Play Server
   After=network-online.target
   Wants=network-online.target

   [Service]
   Type=simple
   User=arc
   WorkingDirectory=/home/arc/Arcaea-server/latest version
   ExecStart=/usr/bin/python3 run_linkplay_server.py

   [Install]
   WantedBy=multi-user.target
   ```
3. Clone this repository, then duplicate `.env-example` to `.env`, and edit the file with the name of your systemd service and the URL of your Discord webhook.
   ```bash
   git clone https://github.com/burritosoftware/arcaea-linkplay-webhook.git
   cd arcaea-linkplay-webhook
   cp .env-example .env
   nano .env
   ```
4. Install the requirements. Then, start the watcher, create a Link Play room, and verify that a message was sent.
   ```bash
   python3 -m pip install -U -r requirements.txt
   python3 watcher.py
   ```
5. If it all looks good, it's best to create a systemd service for this too, like `arcaea-notif.service` at `/etc/systemd/system`:
   ```ini
   [Unit]
   Description=Arcaea Linkplay Webhook
   After=network-online.target
   Wants=network-online.target

   [Service]
   Type=simple
   User=arc
   WorkingDirectory=/home/arc/arcaea-linkplay-webhook
   ExecStart=/usr/bin/python3 watcher.py

   [Install]
   WantedBy=multi-user.target
   ```
