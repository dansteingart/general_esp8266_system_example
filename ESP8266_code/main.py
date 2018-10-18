import urequests as req
import json
import urandom
import time
sets = json.load(open("network.json"))

site = sets['site']
db   = sets['db']
col  = sets['node']

#Designed for the MakerFocus with Screen
SDA = 4
SCL = 5
RST = 16

from machine import I2C,Pin
import ssd1306
import dht

pm= {}
pm['3'] = 0
pm['8'] = 15
pm['7'] = 13
pm['6'] = 12
pm['SCL'] = 14


i2c = I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

#Enable DHT22
power = Pin(12,Pin.OUT)
power.on()

#Pin that pin
d = dht.DHT22(Pin(0,Pin.IN,Pin.PULL_UP))

sent = "Starting The Thing!"

def writer(string,flush=True,height=0):
    if flush:
        oled.fill(0)
        oled.show()
    oled.text(string,0,height)
    oled.show()

def dhter(o):
    oled.fill(0)
    oled.show()
    oled.text("T: "+str(o['temp']),0,0)
    oled.text("H: "+str(o['hum']) ,0,10)
    oled.show()

def sample(dd):
    data = {}
    try:
        dd.measure()
        temp = dd.temperature()
        hum  = dd.humidity()
        data = {'temp':temp,'hum':hum}
    except Exception as E:
        writer("sensor error")
    return data

def send(o):
    out = {'db':db,'col':col}
    out['data']=o
    try:
        out = req.post(site,data=json.dumps(out)).json()
        dhter(o)
    except:
        writer("upload error")

writer("Fire It Up")

count = 0
done = 9

while True:
    try:
        if count < done:
            sent = ""
            for i in range(count):sent+="."
            writer(sent,flush=False,height=20)
            count+=1
        else:
            count = 0
            data = sample(d)
            send(data)
    except Exception as E:
        print(str(E))
    time.sleep(1)
