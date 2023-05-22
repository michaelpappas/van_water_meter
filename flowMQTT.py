import machine
import utime
import network
import time
from umqtt.simple import MQTTClient

# Configure network connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,WIFI_PASSWORD)
time.sleep(5)
print(wlan.isconnected())

# Configure MQTT
mqtt_server = "192.168.1.86"
client_id = 'bigles'
topic_pub = b'water'
topic_msg = b'Movement Detected'

# Configure GPIO pins
flow_pin = machine.Pin(15, machine.Pin.IN)

# Configure variables
flow_frequency = 0
liters_p_minute = 0.0
total_liters = 0.0
start_time = utime.ticks_ms()

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

# Main loop to calculate and print total water flow
while True:
    # Calculate liters per minute based on flow frequency
    # liters_p_minute = flow_frequency / 7.5
    liters_p_minute = flow_frequency / 142.5

    # Calculate total liters based on liters per minute and elapsed time
    current_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(current_time, start_time) / 1000
    total_liters += (liters_p_minute / 60) * elapsed_time

    # Print total liters and reset flow frequency
    print("Total water flow: {:.2f} liters".format(total_liters))
    flow_frequency = 0
    message = f"{total_liters}".encode()
    # Delay for 5 second
    utime.sleep(5)
    # Send total_liters to MQTT Broker
    client.publish(topic_pub, message)
