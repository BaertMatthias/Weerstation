from LCD import LCD
from DbClass import DbClass
import Adafruit_DHT
import RPi.GPIO as GPIO
import datetime

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

humidity = round(humidity, 2)
temperature = round(temperature, 2)

import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

def readChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8 | adc[2])
    return data

def berekenLichtsterkte():
    data_licht = readChannel(0)
    lichtsterkte = -(data_licht - 850)
    lichtsterkte = lichtsterkte / (850 - 180) * 100
    lichtsterkte = round(lichtsterkte,2)
    return lichtsterkte

import Adafruit_BMP2.BMP280 as BMP280

sensor = BMP280.BMP280()
luchtdruk = sensor.read_pressure()
luchtdruk = round(luchtdruk,2)

lcd = LCD(26,19,12,16,20,21)
lcd.main()
lcd.init()
lcd.message('Aangesloten')

db = DbClass()

try:
    while True:
        tijdstip = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        setTempToDatabase(temperature,tijdstip)
        setLightToDatabase(berekenLichtsterkte(),tijdstip)
        setPressureToDatabase(luchtdruk,tijdstip)
        setHumidityToDatabase(humidity,tijdstip)
        time.sleep(1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()

