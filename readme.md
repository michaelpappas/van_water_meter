# Van Water Meter Sensor
A Micropython script that starts monitors when water is passing through a flow meter and send that flow amount in gallons to an MQTT client running on a Raspberry Pi for a van systems dashboard.


## Table of Contents
- [Manual Installation](#manual-installation)
- [Dev Environment](#development-environment)
- [Wiring](#wiring)
- [Further Improvements](#further-improvements)


## Manual Installation

Clone the repo:

```bash
git clone https://github.com/michaelpappas/WATER_TANK_SENSOR
cd WATER_TANK_SENSOR
```

replace the SSID and PASSWORD values with your own wifi SSID and Password.


## Wiring



### Running the Script




## Project Structure

```
\                           # project directory
 |--.env.example            # example environment variables
 |--mqttClient.py           # main MQTT Client
 |--models.py               # models for battery and water tank data
 |--app.py                  # flask app for water consumption reset endpoint
 |--requirements.txt        # script requirements

```

## Further Improvements

1. Complete readme.md










