import RPi.GPIO as GPIO
import time
import socket
import fcntl
import struct
from subprocess import *
RS = 26
E = 19
D4 = 12
D5 = 16
D6 = 20
D7 = 21
lijst_pinnen = [D7,D6,D5,D4]
l_delay = 0.005
s_delay = 0.0002



class LCD:


    def __init__(self,RS,E,D4,D5,D6,D7):
        self.__D7 = D7
        self.__D6 = D6
        self.__D5 = D5
        self.__D4 = D4
        self.__E = E
        self.__RS = RS
        self.__lijst_pinnen = [self.__D7, self.__D6, self.__D5, self.__D4]

    def main(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__RS, GPIO.OUT)
        GPIO.setup(self.__E, GPIO.OUT)
        for i in range(len(self.__lijst_pinnen)):
            GPIO.setup(self.__lijst_pinnen[i], GPIO.OUT)

    def __setGPIODataBits(self,data):
        filterbit = 0x80
        for i in range(len(self.__lijst_pinnen)):
            resultaat = data & filterbit
            if (resultaat == 0):
                GPIO.output(self.__lijst_pinnen[i],GPIO.LOW)
            else:
                GPIO.output(self.__lijst_pinnen[i],GPIO.HIGH)
            data = data << 1
            time.sleep(s_delay)

    def __function_set(self,data):
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)
        data = data << 4
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)

    def __function_set8(self,data):
        #0x38
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)
        data = data << 4
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)

    def __display_on(self,data):
        #0x0F
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)
        data = data << 4
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)

    def __display_off(self,data):
        #0x08
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(s_delay)
        data = data << 4
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()

    def __clear_display(self,data):
        #0x01
        self.__eHoogInstructie()
        self.__setGPIODataBits(0x01)
        self.__eLaagInstructie()
        time.sleep(0.1)
        data = data << 4
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)

    def __eHoogData(self):
        GPIO.output(self.__E,GPIO.HIGH)
        GPIO.output(self.__RS,GPIO.HIGH)

    def __eLaagData(self):
        GPIO.output(self.__E, GPIO.LOW)
        GPIO.output(self.__RS, GPIO.HIGH)

    def __eHoogInstructie(self):
        GPIO.output(self.__E, GPIO.HIGH)
        GPIO.output(self.__RS, GPIO.LOW)

    def __eLaagInstructie(self):
        GPIO.output(self.__E, GPIO.LOW)
        GPIO.output(self.__RS, GPIO.LOW)

    # @staticmethod
    # def reset():
    #     eHoogData()
    #     setGPIODataBits(0x30)
    #     eLaagData()
    #     time.sleep(l_delay)
    #     eHoogData()
    #     setGPIODataBits(0x30)
    #     eLaagData()
    #     time.sleep(s_delay)
    #     eHoogData()
    #     setGPIODataBits(0x30)
    #     eLaagData()
    #     function_set8(0x38)
    #     display_off(0x08)
    #     clear_display(0x01)

    def init(self):
        self.__function_set(0x28)
        self.__display_on(0x0F)
        self.__clear_display(0x01)

    def move_cursor(self):
        # 20
        data = 20
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)
        data = data << 4
        self.__eHoogInstructie()
        self.__setGPIODataBits(data)
        self.__eLaagInstructie()
        time.sleep(0.1)

    def message(self,tekst):
        for i in range(len(tekst)):
            letter = str(tekst[i])
            ascii = ord(letter)
            self.__eHoogData()
            self.__setGPIODataBits(ascii)
            self.__eLaagData()
            time.sleep(0.1)
            ascii = ascii << 4
            self.__eHoogData()
            self.__setGPIODataBits(ascii)
            self.__eLaagData()

# def get_interface_ipaddress(network):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     return socket.inet_ntoa(fcntl.ioctl(
#         s.fileno(),
#         0x8915,
#         struct.pack('256s', network[:15])
#     )[20:24])

cmd = "ip addr show dev eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

ipadres = run_cmd(cmd)
ipadres = ipadres[:13]
print(ipadres)

lcd = LCD(26,19,12,16,20,21)
lcd.main()
lcd.init()
lcd.message('%s' % ( ipadres ))
for i in range(24):
    lcd.move_cursor()
lcd.message('opdracht.py')
try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.output(RS, GPIO.LOW)
    GPIO.output(E, GPIO.LOW)
    for i in range(len(lijst_pinnen)):
        GPIO.output(lijst_pinnen[i], GPIO.LOW)

GPIO.cleanup()