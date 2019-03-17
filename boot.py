# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)


#boot.py
import gc
import network
import ubinascii
import webrepl

print('[boot]')

SSID = '<fillme>'
password = '<fillme>'

wlan = network.WLAN(network.STA_IF) # STA_IF means station interface
ap = network.WLAN(network.AP_IF)    # AP_IF means access point
print('Shutting down access point...')
ap.active(False)    # shut down access point

if not wlan.isconnected():
    print('Connecting to wifi network...')
    wlan.active(True)
    wlan.connect(SSID, password)
    while not wlan.isconnected():
        pass

(ip, netmask, gateway, dns) = wlan.ifconfig()

webrepl.start()
gc.collect()

print('[boot] - DONE')

