import json
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def do_connect(ssid,passw):
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, passw)
        while not wlan.isconnected(): pass
        
try:
    print("Trying to Connect to Network")
    sets = json.load(open("network.json"))
    do_connect(sets['ssid'],sets['pass'])
    print("Connected!")
    print('network config:', wlan.ifconfig())

except Exception as E:
    print("error:")
    print(str(E))
