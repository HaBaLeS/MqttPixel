import machine
import neopixel
from umqtt.simple import MQTTClient
import ubinascii

SERVER="192.168.1.4"
USER="mqtt_user"
PASS="mqtt_pass"
SUB_TOPIC="pixelbrett/cmd/#"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
ANNOUNCE_TOPIC="homeassistant/light/pixelbrett/config"


def all_pixel(r,g,b):
    for i in range(0, pixels.n):
        pixels[i] = (r,g,b)
    pixels.write()

def mqtt_cb(topic, msg):
    print((topic, msg))
    if msg == b"ON":
        all_pixel(0,100,0)
        updateState("light", msg)
    elif msg == b"OFF":
        all_pixel(0,0,0)
        updateState("light", msg)

def updateState(type, msg):
    mqtt_c.publish("pixelbrett/state/"+type,msg)

def start_mqtt_sub(c):
    c.subscribe(SUB_TOPIC)
    print("Connected to %s, subscribed to %s topic" % (SERVER, SUB_TOPIC))
    try:
        while 1:
            c.wait_msg()
    finally:
        c.disconnect()


def mqtt_init():
    c = MQTTClient(client_id=CLIENT_ID, server=SERVER, user=USER, password=PASS)
    c.set_callback(mqtt_cb)
    c.connect()
    return c

def mqtt_publish_device(c):
    msg = """
    {
        "name":"pixelbrett",
        "device_class": "light",
        "state_topic": "pixelbrett/state/light",
        "command_topic": "pixelbrett/cmd/light",
        "brightness_command_topic": "pixelbrett/cmd/brightness",
        "brightness_state_topic": "pixelbrett/state/brightness"
    }
    """
    c.publish(ANNOUNCE_TOPIC,msg)



#ransom Text to make file bigger!!!!

pixels = neopixel.NeoPixel(machine.Pin(4), 5*19)
all_pixel(20,20,20);
mqtt_c = mqtt_init()
mqtt_publish_device(mqtt_c)
start_mqtt_sub(mqtt_c)
