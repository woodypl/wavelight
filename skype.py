import Skype4Py
from urllib import urlopen
from phue import *

HOST = "127.0.0.1"
PORT = 8000
USER = "undefined"
BRIDGE_IP = "FILLMEIN"
BRIDGE_USERNAME = "FILLMEINTOO"

HANDLE1 = "FILL"
HANDLE2 = "ALL"
WWWHANDLE = "THIS"
bulb = None

def user_status(User, Status):
	print("User {0} status changed to {1}".format(User.Handle, Status))
	if User.Handle == HANDLE1:
		bulb = bulb1
	elif User.Handle == HANDLE2:
		bulb = bulb2
	elif User.Handle == WWWHANDLE:
		with open("STATUSFILE.txt", "w") as logfile:
			logfile.write(Status)
		return
	else:
		return
	if Status == "AWAY":
		hue = 12750
	elif Status == "ONLINE":
		hue = 24210
	elif Status == "DND":
		hue = 65535
	elif Status == "OFFLINE" or Status == "INVISIBLE":
		bulb.on = False
		return
	bulb.hue = hue
	bulb.sat = 255
	bulb.brightness = 127
	bulb.on = True
        #urlopen("http://{0}:{1}/skype?id={2}&status={3}".format(HOST, PORT, USER, Status))

bridge = Bridge(BRIDGE_IP, BRIDGE_USERNAME)
bridge.connect()

print( bridge.get_light_objects('name') )

bulb1 = bridge.get_light_objects('name')['Rod']
bulb2 = bridge.get_light_objects('name')['Door']

# Create an instance of the Skype class.
skype = Skype4Py.Skype()

# Connect the Skype object to the Skype client.
skype.Attach()

#USER = skype.CurrentUser.Handle

skype.OnOnlineStatus = user_status
user_status(skype.User(HANDLE1), skype.User(HANDLE1).OnlineStatus)
user_status(skype.User(HANDLE2), skype.User(HANDLE2).OnlineStatus)
user_status(skype.User(WWWHANDLE), skype.User(WWWHANDLE).OnlineStatus)

print("Skype status notifier running in a loop. Hit CTRL-C to quit.")

import time
while True:
    time.sleep(1)
