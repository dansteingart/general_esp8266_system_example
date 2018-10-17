import urequests as req
import json
import urandom
import time
site="https://data.dansteingart.com/input/"
SDA = 4
SCL = 5
RST = 16
import machine
import ssd1306
import dht

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
#Turn Power On
power = machine.Pin(13,machine.Pin.OUT)
power.on()

#Enable DHT22
d = dht.DHT22(machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_UP))

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
    out = {'db':'lab_data','col':'ACEE214'}
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
