# rocketWebUI and rocketXbeeConnection

Uses Python and JavaScript to procces data and chart in real time.

## rocketWebUI

### How to use

Start Python webserver:

```python
python3 -m http.server:3000
```

Start Python script:

```python
python3 websocket_server.py
```

### Libraries and other resources used

#### Python

- tornado

#### JavaScript

- d3.js
- dc.js
- crossfilter.js

## rocketXbeeConnection

- ### rocketXbeeClient

  - rocketXbeeClient is the ground station laptop and will mainly be receving data from the rocket xbee radio.

- ### rocketXbeeServer

  - rocketXbeeServer is the rocket xbee radio and will mainly be sending data to the ground station.
