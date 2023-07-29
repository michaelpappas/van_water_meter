# Van Water Meter Sensor
A Micropython script that starts monitors when water is passing through a flow meter and send that flow amount in gallons to an MQTT client running on a Raspberry Pi for a van systems dashboard.
This uses a [GR-301](https://www.amazon.com/GREDIA-Connect-Food-Grade-Flowmeter-Counter/dp/B07MY7H45V) flow meter but should also work well with the generic YS-201 or most hall effect sensors.


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
Flow meter ground -> pi GPIO3
Flow meter VCC -> pi GPIO5
Flow meter signal out -> pi GPIO15

### Running the Script




## Project Structure

```
\                           # project directory
 |--flowMQTT.py             # micropython script for sensing water volume and mqtt
 |--readme.md               # project readme

```

## Further Improvements

1. Complete readme.md
2. Configure script to run automatically when pi gets power










