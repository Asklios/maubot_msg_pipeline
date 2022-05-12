# Maubot-Plugin for the Message-Pipeline
![Languages](https://img.shields.io/github/languages/top/Asklios/maubot_msg_pipeline.svg)
![Modified](https://img.shields.io/github/last-commit/Asklios/maubot_msg_pipeline.svg)
[![Release](https://img.shields.io/github/release/Asklios/maubot_msg_pipeline.svg)](https://github.com/Asklios/maubot_msg_pipeline/releases)
[![License](https://img.shields.io/github/license/Asklios/maubot_msg_pipeline.svg)](https://github.com/Asklios/maubot_msg_pipeline/blob/master/LICENSE)
![TotalLines](https://img.shields.io/tokei/lines/github/Asklios/maubot_msg_pipeline.svg)

_by_ [_Asklios_](https://github.com/Asklios)

## What is it?
This is a Maubot plugin that connects to a SocketIO server and forwards messages to preconfigured matrix rooms.
Message replies and deletions are supported.

## How to use it?
1. You will need the [backend](https://github.com/Asklios/msg-pipeline) up and running so start there. There is also a 
Docker image available, just check out the repo.
2. Download the latest release of the plugin and upload it to your Maubot instance. You can find detailed instructions 
on how to do that [here](https://docs.mau.fi/maubot/index.html).
3. Add your api-key and url to the config.
4. Configure the rooms you want to forward to. You can add as many as you want. On the left side 
you set the alias or id you will use when using the rest api. On the right side, set the matrix room-id or room-alias. 
If you don't receive any messages, doublecheck the matrix room-alias or room-id.