import machine
import neopixel
from umqtt.simple import MQTTClient
import ubinascii

import device_config as cfg


class HomeAssistantMQTTLight:

    def __init__(self):

        self.brightness=100
        self.c_red=100
        self.c_green=100
        self.c_blue=100

        self.mqtt_c = None
        self.pixels = neopixel.NeoPixel(machine.Pin(4), cfg.PIXEL_COUNT)

    def all_pixel(self,r,g,b):
        f = self.brightness/255
        for i in range(0, self.pixels.n):
            self.pixels[i] = (int(r*f),int(g*f),int(b*f))
        self.pixels.write()

    def mqtt_cb(self,topic, msg):
        msg=str(msg,"ANSII")
        print((topic, msg))

        if "brightness" in topic:
            self.brightness=int(msg)
            self.all_pixel(self.c_red, self.c_green, self.c_blue)
            self.updateState("brightness", self.brightness)
        if "color" in topic:
            r, g, b = str(msg).split(',')
            self.c_red = int(r)
            self.c_green = int(g)
            self.c_blue = int(b)
            self.all_pixel(self.c_red, self.c_green, self.c_blue)
            self.updateState("color", msg) #cheated with the color string
        if msg == "ON":
            self.all_pixel(self.c_red, self.c_green, self.c_blue)
            self.updateState("light", msg)
        elif msg == "OFF":
            self.all_pixel(0,0,0)
            self.updateState("light", msg)

    def updateState(self, type, msg):
        self.mqtt_c.publish(cfg.DEVICE_NAME + "/state/"+type, str(msg))

    def start_sub(self):
        self.mqtt_c.subscribe(cfg.SUB_TOPIC)
        print("Connected to %s, subscribed to %s topic" % (cfg.SERVER, cfg.SUB_TOPIC))
        try:
            while 1:
                self.mqtt_c.wait_msg()
        finally:
            self.mqtt_c.disconnect()


    def init_mqtt(self):
        self.mqtt_c = MQTTClient(client_id=cfg.CLIENT_ID, server=cfg.SERVER, user=cfg.MQTT_USER, password=cfg.MQTT_PASS)
        self.mqtt_c.set_callback(self.mqtt_cb)
        self.mqtt_c.connect()

    def publish_device(self):
        msg = """
        {
            "name":"<dev_name>",
            "device_class": "light",
            "state_topic": "<dev_name>/state/light",
            "command_topic": "<dev_name>/cmd/light",
            "brightness_command_topic": "<dev_name>/cmd/brightness",
            "brightness_state_topic": "<dev_name>/state/brightness",
            "brightness_scale": 255,
            "rgb_command_topic": "<dev_name>/cmd/color",
            "rgb_state_topic": "<dev_name>/state/color"
        }
        """
        msg = msg.replace("<dev_name>", cfg.DEVICE_NAME)
        self.mqtt_c.publish(cfg.ANNOUNCE_TOPIC,msg)

hawl = HomeAssistantMQTTLight()
hawl.all_pixel(20,20,20);
hawl.init_mqtt()
hawl.publish_device()
#hawl.start_mqtt_sub()
