#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time
import sys
import os
import Tkinter  
import os, urlparse
import datetime
from Tkinter import *

#fill your cloud mqtt credentials here
PUBLISH_TOPIC = ""
BROKER_URL = ""
BROKER_PORT = 
BROKER_USERNAME = ""
BROKER_PASSWORD = ""
SUBSCRIBE_TOPIC = ""

class Home_automation:
    def __init__( self ):
        self.client = mqtt.Client()
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
        self.client.connect(BROKER_URL, BROKER_PORT, 120)
        self.client.subscribe(SUBSCRIBE_TOPIC, qos=1)
            
    # def button_select_call(self):
    #     pass
    #   # self.PUBLISH_TOPIC=self.serial_number_entry.get()

    def red_on(self):
        self.msg="florida"
        self.publish_command()
        # self.subscription()

    def green_on(self):
        self.msg="california"
        self.publish_command()
        # self.subscription()


    def fetch_sensor_data(self):
        # self.msg="turn_off"
        # self.publish_command()
        self.subscription()

    def set_relay_state(self):
        self.msg=str(self.action_entry.get())
        self.publish_command()
        # self.subscription()

    def publish_command(self):
      try:
        print "*******************command_published************************"
        print "payload :", self.msg
        print "topic details:",PUBLISH_TOPIC,BROKER_URL ,BROKER_PORT ,BROKER_USERNAME ,BROKER_PASSWORD 
        (rc, mid) = self.client.publish(PUBLISH_TOPIC,self.msg, qos=1) #mid updates on each publish
        if rc != 0:
            self.client.on_connect = self.on_connect
            print "rc:" ,rc
        print "mid:" ,mid
        print "published to :",PUBLISH_TOPIC
        print "**************************************************"
        return True
      except Exception as e:
        print str(e)
        return False

    def on_connect(self, client, userdata, rc):
        print("Connected with result code "+str(rc))
        self.client.loop_start()

    def on_publish(self, client, userdata, mid):
        print("mid: "+str(mid))

    def loop_start(self):
        self.client.loop_start()

    def on_connect_sb(self,mosq, client, userdata, rc):
        print("rc: " + str(rc))

    def on_subscribe(self,mosq, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self,mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        self.pressure_entry.delete(0,END)
        self.pressure_entry.insert(INSERT,str(msg.payload))

    def subscription(self):
        print "starting subscriber"
        try:
            rc = 0
            i=0
            while rc==0:
                if i<5:
                    rc = self.client.loop()
                    i=i+1
                elif i>4:
                    i=0
                    break
            print("rc: " + str(rc))
        except Exception as err:
            print str(err)
            pass

    def run(self):
        root=Tk()
        frame=Frame(root,bg='green')
        frame.pack()
        root.title("mqtt_demonstration")
        #LABELS
        self.space_label=Label(frame,text="          ",bg="green",fg="black")
        self.space_label.grid(row=0,column=0,sticky=NS)

        self.space_label=Label(frame,text="     ",bg="green",fg="black")
        self.space_label.grid(row=1,column=1,sticky=NS)


        self.pressure_label=Label(frame,text="subscribed data",bg="green",fg="black")
        self.pressure_label.grid(row=3,column=0,sticky=NS)
        self.pressure_entry=Entry(frame)
        self.pressure_entry.grid(row=3,column=1,sticky=NS)
        self.pressure_entry.insert(INSERT,"subscribe")

        self.get_sensor_data=Button(frame, text="subscribe", command=self.fetch_sensor_data, fg="BLACK")
        self.get_sensor_data.grid(row=3,column=2,sticky=W)

        self.space_label=Label(frame,text="          ",bg="green",fg="black")
        self.space_label.grid(row=4,column=0,sticky=NS)


        self.action_label=Label(frame,text="set relay state",bg="green",fg="black")
        self.action_label.grid(row=5,column=0,sticky=NS)
        self.action_entry=Entry(frame)
        self.action_entry.grid(row=5,column=1,sticky=NS)
        self.get_sensor_data=Button(frame, text="publish", command=self.set_relay_state, fg="BLACK")
        self.get_sensor_data.grid(row=5,column=2,sticky=NS)

        self.space_label=Label(frame,text="          ",bg="green",fg="black")
        self.space_label.grid(row=6,column=0,sticky=NS)

        self.toggle_label=Label(frame,text="publish hardcoded",bg="green",fg="black")
        self.toggle_label.grid(row=7,column=0,sticky=NS)
     
        self.green_button=Button(frame, text="california", command=self.green_on, fg="BLACK")
        self.green_button.grid(row=7,column=1,sticky=NS)
        self.red_button=Button(frame, text="florida", command=self.red_on, fg="BLACK")
        self.red_button.grid(row=7,column=2,sticky=NS)

        root.mainloop()
        

def run():
    time.sleep(2)
    sw= Home_automation()
    sw.run()
    time.sleep(.1)

if __name__ == "__main__":
    run()
