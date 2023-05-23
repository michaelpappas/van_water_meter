import machine
import utime
import network
import time
from umqtt.simple import MQTTClient

# Configure network connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssdi,password)
time.sleep(5)
print(wlan.isconnected())

# Configure MQTT
mqtt_server = "192.168.1.86"
client_id = 'michael'
topic_pub = b'water/total'

# Set water_value for global use
water_value = 0.0

# Configure GPIO pins
flow_pin = machine.Pin(15, machine.Pin.IN)

# Configure water flow variables
flow_frequency = 0
liters_p_minute = 0.0
total_liters = 0.0
start_time = utime.ticks_ms()
FLOW_CALIB = 142.5

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
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()


def callback(topic, msg):
    global water_value
    if topic == b"water/connect":
        print(msg.decode())
        water_value = float(msg.decode())
        print(f"Water value received from broker, {water_value}")
    if topic == b"water/reset":
        water_value = float(0)
        print("water value reset")

client.set_callback(callback)
client.subscribe("water/#")
# utime.sleep(10)

# Main loop to calculate and print total water flow
while True:

    client.check_msg()
    # Calculate liters per minute based on flow frequency

    liters_p_minute = flow_frequency / FLOW_CALIB

    # Calculate total liters based on liters per minute and elapsed time
    current_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(current_time, start_time) / 1000
    total_liters += (liters_p_minute / 60) * elapsed_time

    water_value = water_value + total_liters
    total_liters = 0

    # Print water_value and reset flow frequency
    print("Total water flow: {:.2f} liters".format(water_value))
    flow_frequency = 0
    message = f"{water_value}".encode()

    # Delay for 5 second
    utime.sleep(5)

    # Send total_liters to MQTT Broker
    client.publish(topic_pub, message)
