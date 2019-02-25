#netmonpizw
#A script for network continuity monitoring utilizing a Raspberry Pi Zero W and Blinkt! LED indicators

import os
import threading
from collections import deque
import blinkt #Required, run "pip install blinkt"

#Script Variables
UnlitMode = True;   #Low impact mode toggles whether indicator for having internet is lit LED's or off ones.
ScanInterval = 1.0  #How often ping is sent and LED's are updated in seconds.
Brightness = .09    #Brightness of all lit LED's
LEDQueue = deque(["", "", "", "", "", "", "", ""]) #Initialize deque list, holds LED colors.

#Color Definition
col_Red = [255, 0, 0];
col_Green = [0, 255, 0];
col_Blue = [0, 0, 255];

def main():
    update()

def check_ping(): #Pings host for response. Returns response.
    hostname = "8.8.8.8" #Target to ping
    response = os.system("ping -c 1 -O -q " + hostname) #Send Ping
    #Check ping response (for testing):
    '''
    if response == 0:
        pingstatus = response
    else:
        pingstatus = "Destination: " + hostname + " unreachable."
    print("pingstatus")
    '''
    return response

def updateblinkt(): #Takes values stored in LEDQueue, translates them to r,g,b, assigns, and shows them.

    blinkt.clear() #Clear LED statuses.

    for i in range(0, len(LEDQueue), 1):
        #print(str(i) + ": " + LEDQueue[i]) #For testing, prints LEDQueue light statuses.

        #Translate color strings to (r,g,b) values, defined above.
        if (LEDQueue[i] == "green"):
            if(not UnlitMode):
                blinkt.set_pixel(i, col_Green[0], col_Green[1], col_Green[2], Brightness) #Light LED green.
            else:
                blinkt.set_pixel(i, col_Green[0], col_Green[1], col_Green[2], 0) #Store Value but keep LED unlit.
        elif (LEDQueue[i] == "red"):
            blinkt.set_pixel(i, col_Red[0], col_Red[1], col_Red[2], Brightness)
        else:
            blinkt.set_pixel(i, col_Blue[0], col_Blue[1], col_Blue[2], Brightness)

    blinkt.show() #Show updates on Blinkt


def update(): #Method for continous scanning and updating
    threading.Timer(ScanInterval, update).start() #Start repeating scan.

    #Check ping for positive results.
    if (check_ping() == 0):
        LEDQueue[0] = "green" #Store positive result in LEDqueue.
    else:
        LEDQueue[0] = "red" #Store negative result in LEDqueue.

    updateblinkt()
    LEDQueue.rotate(1)


if __name__ == '__main__':
    main()
