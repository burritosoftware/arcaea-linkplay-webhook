# arcaea-linkplay-webhook
![Icons](https://skillicons.dev/icons?i=py,linux,discord)

[![WakaTime](https://wakatime.com/badge/github/burritosoftware/arcaea-linkplay-webhook.svg)](https://wakatime.com/badge/github/burritosoftware/arcaea-linkplay-webhook)

---

## How this works
This script reads the logs for [Arcaea-server](https://github.com/Lost-MSth/Arcaea-server)'s Link Play server, running in a systemd unit.
It parses log messages for new rooms and sends a nicely-formatted message in Discord, announcing them and any players that join.

![Preview](https://taidums.are-really.cool/5zReRDx.png)

## Limitations
Unfortunately, [Arcaea-server](https://github.com/Lost-MSth/Arcaea-server)'s Link Play server does not print log messages when the host of a room changes, or when players leave/the room is closed. Therefore, the messages sent by this webhook won't be edited if a player leaves or the room is closed.
