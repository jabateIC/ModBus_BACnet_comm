import BAC0
import bacpypes
import time
from collections import namedtuple
from BAC0.core.devices.local.models import (
    analog_input,
    analog_output,
    analog_value,
    binary_input,
    binary_output,
    binary_value,
    multistate_input,
    multistate_output,
    multistate_value,
    date_value,
    datetime_value,
    temperature_input,
    temperature_value,
    humidity_input,
    humidity_value,
    character_string,
)
from BAC0.core.devices.local.object import ObjectFactory
from BAC0.core.devices.local.models import make_state_text

def add_points(qty_per_type, device):
    # Start from fresh
    ObjectFactory.clear_objects()
    basic_qty = qty_per_type - 1
    # Analog Inputs
    # Default... percent
    for _ in range(basic_qty):
        _new_objects = analog_input(presentValue=99.9)
        _new_objects = multistate_value(presentValue=1)

    # All others using default implementation
    for _ in range(qty_per_type):
        _new_objects = analog_output(presentValue=89.9)
        _new_objects = analog_value(presentValue=79.9)
        _new_objects = character_string(presentValue="test", is_commandable=True)

    _new_objects.add_objects_to_application(device)

def main():
    # Create Client
    bacnet = BAC0.lite()

    # Create Simulated BACnet devices
    device_app = BAC0.lite(port=47809, deviceId=101)
    device_app2 = BAC0.lite(port=47810, deviceId=102)
    add_points(1, device_app)
    add_points(1, device_app2)
    # locate IP and device ID information
    ip = device_app.localIPAddr.addrTuple[0]
    boid = device_app.Boid
    ip2 = device_app2.localIPAddr.addrTuple[0]
    boid2 = device_app2.Boid

    # Define controllers, this is where I can read and write to the devices that are being simulated
    test_device = BAC0.device("{}:47809".format(ip), boid, bacnet, poll=10)
    test_device2 = BAC0.device("{}:47810".format(ip2), boid2, bacnet, poll=0)

    # small function to populate the simulated bacnet nodes
    while True:
        print(test_device.points)
        time.sleep(2)
        test_device['AV'] *= .95


if __name__ == "__main__":
    main()