#!/bin/bash
open "http://127.0.0.1:3000"
python3 ./rt_data_server/websocket_server.py & python3 -m http.server ./rt_data_server/ && fg
