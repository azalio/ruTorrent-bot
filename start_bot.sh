#!/bin/bash

docker run --detach --restart always --volume rutorrent_user_info:/usr/src/app/chat_id_file rutorrent-bot
