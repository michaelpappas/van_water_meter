# flow meter wiring
# power -> 3v3 GPIO5
# ground -> ground GPIO3
# signal -> GPIO15

import machine
from machine import Pin, I2C
import utime
import network
import time
from umqtt.simple import MQTTClient

# Configure network connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ATT4EcFvWG", "28wws2#v#ayp")
time.sleep(5)
print(wlan.isconnected())

# Configure MQTT
mqtt_server = "192.168.1.86"
client_id = 'water_meter'
topic_pub = b'water/update'

# Set water_value for global use
water_value = 0.0

# Configure GPIO pins
flow_pin = machine.Pin(15, machine.Pin.IN)

# Configure water flow variables
flow_frequency = 0
gallons_p_minute = 0.0
liters_p_minute = 0.0
total_liters = 0.0
total_gallons = 0.0
start_time = utime.ticks_ms()
FLOW_CALIB = 37.64

# Define interrupt function to calculate flow frequency
def handle_interrupt(pin):
    global flow_frequency
    flow_frequency += 1

# Configure interrupt on falling edge of flow sensor signal
flow_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_interrupt)


# Connect to MQTT client
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    client.publish("connect/water", '{"client_id": "water_meter" , "status": "connected}')
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()


# def callback(topic, msg):
#     global water_value
#     if topic == b"connect/water/response":
#         print(msg.decode())
#         water_value = float(msg.decode())
#         print(f"Water value received from broker, {water_value}")
#     if topic == b"water/reset":
#         water_value = float(0)
#         print("water value reset")

# client.set_callback(callback)
# client.subscribe(['water/#', 'connect/#'])
# utime.sleep(10)

# Main loop to calculate and print total water flow

while True:
    # Calculate liters per minute based on flow frequency
    liters_p_minute = flow_frequency / FLOW_CALIB

    # Calculate total liters based on liters per minute and elapsed time
    current_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(current_time, start_time) / 1000
    total_liters += (liters_p_minute / 60) * elapsed_time
    total_gallons = total_liters * .2641

    # Print total liters and reset flow frequency
    print("Total water flow: {:.2f} gallons".format(total_gallons))
    if flow_frequency > 0:
        print("new conspumption", total_gallons)
        data = {"consumption": total_gallons}
        msg = f'{data}'.encode()
        client.publish(topic_pub, msg)
        total_liters = 0
    flow_frequency = 0

    # Delay for 10 second
    utime.sleep(10)

