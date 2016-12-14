import serial
import requests
import time
import json

#### some basic variables


baseURL = 'http://159.203.128.53'
#baseURL = 'https://data.sparkfun.com'

publicKey='parbNrpbjVC9XOMLJArXiMvg0XN'
privateKey='lKZ8yZw8lrIMjdY6qWVjHn7ZaY4'

#serialPort="/dev/ttyACM0"
serialPort="/dev/ttyUSB0"

serialBaud = 9600

loopDelay = 10 #seconds

endl="\n"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

### convenience function for posting to Phant
def postPhant(line):
    x=line.strip()
    x=x.strip()
    x=x.split(",")
    if (len(x)==6):
        timeVar=x[0]
        temp=float(x[1])
        pres=float(x[2]) 
        rh=float(x[3])
        tempc=float(x[4])
        tempf=float(x[5])

        pushUrl = baseURL+'/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&datetime='+str(timeVar)+'&temperature='+str(temp)+'&pressure='+str(pres)+'&humidity='+str(rh)+'&tempc='+str(tempc)+'&tempf='+str(tempf)

        print pushUrl
        push = requests.get(pushUrl)
        
        return push.status_code
        
###### open and flush serial port

ser = serial.Serial(serialPort, serialBaud)

#print "Waiting for serial port ..."
time.sleep(3)
#ser.flush() # flush to get rid of extraneous char

print "\n"

###### main loop 

while True:

    #cmd = "READ"
    #cmd = cmd.strip() + endl
    #ser.write(cmd.encode())
    #print "Waiting for serial port ..."
    
    line = ser.readline()
    line=line.decode('utf-8')
    
    #print 'raw serial input: ', line.strip()
  
    a = line.split(',')
    if len(a)==4 and is_number(a[0]) and is_number(a[1]) and is_number(a[2]) and is_number(a[3]):
        nodeId=a[0]
        temp=a[1]
        humidity=a[2]
        pressure=a[3]

        #print temp,humidity,pressure

        pushUrl = baseURL+'/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&pressure='+str(pressure)+'&temp='+str(temp)+'&humidity='+str(humidity)+'&nodeid='+str(nodeId)

        print pushUrl

        push = requests.get(pushUrl)
        
        print push




