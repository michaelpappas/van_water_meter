import machine
import utime

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

    # Delay for 1 second
    utime.sleep(1)