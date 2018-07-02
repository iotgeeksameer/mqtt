import paho.mqtt.client as mqtt
import time
import sys
import os
import binascii

#fill your cloud mqtt credentials here
PUBLISH_TOPIC = "mock_keyboard"
BROKER_URL = ""
BROKER_PORT = 
BROKER_USERNAME = ""
BROKER_PASSWORD = ""


class Publisher:
    def __init__( self ):    
        self.client = mqtt.Client()
        self.client.loop_start()
        self.client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
        self.client.connect(BROKER_URL, BROKER_PORT, 120)


    def update_and_publish(self,Ax_index,Ay_index,Az_index,Gx_index,Gy_index,Gz_index):
      a0=(int(Ax_index))
      a1=(int(Ay_index))
      a2=(int(Az_index))
      a3=(int(Gx_index))
      a4=(int(Gy_index))
      a5=(int(Gz_index))

      baray=bytearray(32) 
      #device id
      dev_id = 151
      baray[0]=(int(dev_id)&0xff000000)
      baray[1]=(int(dev_id)&0x00ff0000)
      baray[2]=(int(dev_id)&0x0000ff00)
      baray[3]=(int(dev_id)&0x000000ff)

      #access coad = 0001
      a_code = 0001
      baray[4]=(int(a_code)&0xff000000)
      baray[5]=(int(a_code)&0x00ff0000)
      baray[6]=(int(a_code)&0x0000ff00)
      baray[7]=(int(a_code)&0x000000ff)

        # Accelarometer    Ax       
      baray[8]=(int(a0)&0xff000000)
      baray[9]=(int(a0)&0x00ff0000)
      baray[10]=(int(a0)&0x0000ff00)
      baray[11]=(int(a0)&0x000000ff)

      # Accelarometer      Ay
      baray[12]=(int(a1)&0xff000000)
      baray[13]=(int(a1)&0x00ff0000)
      baray[14]=(int(a1)&0x0000ff00)
      baray[15]=(int(a1)&0x000000ff)
      
      # Accelarometer      Az
      baray[16]=(int(a2)&0xff000000)
      baray[17]=(int(a2)&0x00ff0000)
      baray[18]=(int(a2)&0x0000ff00)
      baray[19]=(int(a2)&0x000000ff)
      
       # Gyrometer        Gx
      baray[20]=(int(a3)&0xff000000)
      baray[21]=(int(a3)&0x00ff0000)
      baray[22]=(int(a3)&0x0000ff00)
      baray[23]=(int(a3)&0x000000ff)
      
      # Gyrometer         Gy
      baray[24]=(int(a4)&0xff000000)
      baray[25]=(int(a4)&0x00ff0000)
      baray[26]=(int(a4)&0x0000ff00)
      baray[27]=(int(a4)&0x000000ff)
      
      # Gyrometer         Gz
      baray[28]=(int(a5)&0xff000000)
      baray[28]=(int(a5)&0x00ff0000)
      baray[30]=(int(a5)&0x0000ff00)
      baray[31]=(int(a5)&0x000000ff)

      try:
        print "*******************command_published************************"
        print "payload :", binascii.hexlify(baray)
        (rc, mid) = self.client.publish(PUBLISH_TOPIC, baray, qos=1)
        if rc != 0:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
        print "rc:" ,rc
        print "mid:" ,mid
        print "published to :",PUBLISH_TOPIC
        print "**************************************************"
        time.sleep(.5)
        return True
      except Exception as e:
        print str(e)
        return False

    def on_connect(self, client, userdata, rc):
        print("Connected with result code "+str(rc))
        # self.client.loop_start()


    def on_publish(self, client, userdata, mid):
        print("mid: "+str(mid))
        
    def on_disconnect(self, client, userdata, rc):
      self.client.loop_start();

    
    def loop_start(self):
        self.client.loop_start()

    def run(self):
        i=0
        increasing = 1
        while(1):          
          print "starting publisher" 
          if ((increasing==1) and (i<40)):
            i=i+1          
          elif((increasing==1) and (i == 40)):
            increasing = 0
            i=i-1
          elif((increasing==0) and (i == 0)):
            increasing = 1
            i=i+1
          elif((increasing==0) and (i<40)):
            i=i-1
          
          else:
            print " need debug"
            print "increasing=",increasing
            print" i=",i
          print " value= ", i
          self.update_and_publish(i,i,i,i,i,i); 
          time.sleep(.1)         
        # self.client.loop_start()
          

def run():
    time.sleep(2)
    while (1):
        pb= Publisher()
        pb.run()
        time.sleep(.1)

if __name__ == "__main__":
    run()


#     Accelarometer            Gyrometer
#   Ax       Ay      Az      Gx   Gy   Gz
# -6616    13880    -1380    915    -68    -49
# -6624    13924    -1496    909    -41    -136
# -6680    13896    -1408    917    -46    -148
# -6636    13996    -1508    913    -35    -111
# -6668    13896    -1616    902    -47    -47
# -6716    13944    -1496    916    -43    -40
# -6616    13972    -1412    879    -57    -5
# -6584    13884    -1536    918    -47    -25
# -6920    14192    -1584    892    -10    -164
# -7792    15016    -1524    1022   -80    -68
# -6928    14244    -1484    773    -112    261
# -6396    13764    -1416    939    -72    112
# -6636    14020    -1596    892    -43    -154
# -6520    13836    -1524    946     4    -242
# -6776    13916    -1552    926     8    -333
# -6916    14008    -1568    891    -64   -54
# -6592    13936    -1460    866    -113  216
