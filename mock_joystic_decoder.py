import paho.mqtt.client as mqtt
#import mosquitto
import time
import sys
import os
import binascii
from datetime import datetime

#fill your cloud mqtt credentials here
SUBSCRIBE_TOPIC= "mock_keyboard"
BROKER_URL = ""
BROKER_PORT = 
BROKER_USERNAME = ""
BROKER_PASSWORD = ""


class subscriber:
    def __init__( self ):    
        self.client = mqtt.Client()
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
        self.client.connect(BROKER_URL, BROKER_PORT, 120)
        self.client.subscribe(SUBSCRIBE_TOPIC, qos=1)
        # self.client.loop_start()


    def on_subscribe(self, client, userdata, mid, granted_qos):
        print "Subscribed: ",str(mid)," ",str(granted_qos)
        

    def on_connect(self, client, userdata, rc):
        print"Connected with result code ",str(rc)
        self.client.loop_start()


    def on_message(self, client, userdata, msg):
        response_1=bytearray(msg.payload)
        rsp_len=len(msg.payload)
        print "*******************response/periodic_data************************"
        timestamp=datetime.now()
        print timestamp
        print "qos :", msg.qos
        print "topic :", msg.topic
        print "length of payload :",rsp_len
        print "payload :",binascii.hexlify(msg.payload)
        print "-------------------------------------------------------------------"
        Device_id=((response_1[0]<<24)+(response_1[1]<<16)+(response_1[2]<<8)+response_1[3])
        Access_code=((response_1[4]<<24)+(response_1[5]<<16)+(response_1[6]<<8)+response_1[7])
            

        Ax=((response_1[8]<<24)+(response_1[9]<<16)+(response_1[10]<<8)+response_1[11])
        Ay=((response_1[12]<<24)+(response_1[13]<<16)+(response_1[14]<<8)+response_1[15])
        Az=((response_1[16]<<24)+(response_1[17]<<16)+(response_1[18]<<8)+response_1[19])

        Gx=((response_1[20]<<24)+(response_1[21]<<16)+(response_1[22]<<8)+response_1[23])
        Gy=((response_1[24]<<24)+(response_1[25]<<16)+(response_1[26]<<8)+response_1[27])
        Gz=((response_1[28]<<24)+(response_1[29]<<16)+(response_1[30]<<8)+response_1[31])
       

        print "Device_id=",Device_id
        print "Access_code=",Access_code
        print "Ax=",Ax
        print "Ay=",Ay
        print "Az=",Az
        print "Gx=",Gx
        print "Gy=",Gy
        print "Gz=",Gz
        print "**************************************************************"

    
    def loop_start(self):
        self.client.loop_start()

    def run(self):        
        self.client.loop_start()
          

def run():
    sb= subscriber()
    print "starting subscriber" 
    while (1):  
      sb.run()   
      time.sleep(.1)   
    

if __name__ == "__main__":
    run()
