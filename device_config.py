import ubinascii
import machine

DEVICE_NAME="pixelbrett"
PIXEL_COUNT=19

SERVER="192.168.1.4"
MQTT_USER="mqtt_user"
MQTT_PASS="mqtt_pass"
SUB_TOPIC= DEVICE_NAME +"/cmd/#"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
ANNOUNCE_TOPIC="homeassistant/light/" + DEVICE_NAME + "/config"
