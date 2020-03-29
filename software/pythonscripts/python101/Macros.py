#!/usr/bin/python3.8
from ctypes import windll, Structure, c_long, byref
import pyautogui
import socket
import datetime
import python101

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

#Variables for fingers - 10 sensors, each finger has 2
flexFinger1 = python101.data["Thumb_0"]
flexFinger2 = python101.data["Thumb_1"]
flexFinger3 = python101.data["IndexF_tip"]
flexFinger4 = python101.data["IndexF_0"]
flexFinger5 = python101.data["MiddleF_tip"]
flexFinger6 = python101.data["MiddleF_0"]
flexFinger7 = python101.data["RingF_tip"]
flexFinger8 = python101.data["RingF_0"]
flexFinger9= python101.data["LittleF_tip"]
flexFinger10 = python101.data["LittleF_0"]

gloveActivated = True
indexSplitMessage=0
gloveActivatedFinger=0

thumb = False
indexFinger = False
middleFinger = False
ringFinger = False
littleFinger = False

thumbHalf = False
indexHalf = False
middleHalf = False
ringHalf = False
littleHalf = False

thumbMacro="";
indexMacro="";
middleMacro="";
ringMacro="";
littleMacro="";

#Variables for touch sensors
touchFinger1 = 0
touchFinger2 = 0
touchFinger3 = 0
touchFinger4 = 0

#Variable rotation time
timeRotation = 0

#Variables rotation
rotationXaxis = 0
rotationYaxis = 0
rotationZaxis = 0

#Variables acceleration
accelerationTime = 0
accelerationXaxis = 0
accelerationYaxis = 0
accelerationZaxis = 0

#socket
listensocket=socket.socket()
Port=8000
maxConnections=999
IP=socket.gethostname()

listensocket.bind(('',Port))

listensocket.listen(maxConnections);
print("server started at "+IP+" on port "+str(Port))

(clientsocket, address)=listensocket.accept()
print("New connection made!")


def RightMouseClick():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    pyautogui.rightClick(x=pt.x, y=pt.y)

def LeftMouseClick():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    pyautogui.Click(x=pt.x, y=pt.y)

def ClosePage():
    pyautogui.hotkey('ctrl', 'w')  

def Copy():
    pyautogui.hotkey('ctrl', 'c')  

def Paste():
    pyautogui.hotkey('ctrl', 'v')

def PrintScreen():
    pyautogui.hotkey('ctrl', 'PrtSc') 

def CloseCommandPrompt():
    pyautogui.hotkey("esc")

def Save():
    pyautogui.hotkey('ctrl','s')

def Undo():
    pyautogui.hotkey('ctrl','z')

def Refresh():
    pyautogui.hotkey('F5')

def SelectAll():
    pyautogui.hotkey('ctrl','a')

def Cut():
    pyautogui.hotkey('ctrl','x')

def Bold():
    pyautogui.hotkey('ctrl','b')

def PauseGlove():
    if(gloveActivated==True): 
        print("Glove OFF")
        gloveActivated=False
    elif(gloveActivated==False): 
        print("Glove ON")
        gloveActivated=True

def CheckFingers():
    #the indexfinger is bend when the value of the flex resistor (2 flex sensors on each finger) is larger than 200 for each
    if(flexFinger1>=200 and flexFinger2>=200):
        thumb=True
    else:
        thumb=False
    if(flexFinger3>= 200 and flexFinger4>=200):
        indexFinger=True
    else:
        indexFinger=False
    if(flexFinger5>=200 and flexFinger6>=200):
        middleFinger=True
    else:
        middleFinger=False

    if(flexFinger7>=200 and flexFinger8>=200):
        ringFinger=True
    else:
        ringFinger=False

    if(flexFinger9>=200 and flexFinger10>=200):
        littleFinger=True
    else:
       littleFinger=False

while True:

    #update values from the Bluetooth
    python101.update()

    CheckFingers()

    #socket-message
    message=clientsocket.recv(1024).decode()
    if(message!=""):
        SplitMessage=message.split("-")


    for macro in SplitMessage:
        if(macro == "PauseGlove"):
            gloveActivatedFinger = indexSplitMessage
        indexSplitMessage = indexSplitMessage + 1


    #when you bend the thumb the glove is paused, if you bend it again, the glove is back on.
    if(gloveActivatedFinger==0):
        if(thumb):PauseGlove();
    elif(gloveActivatedFinger==1):
        if(indexFinger):PauseGlove();
    elif(gloveActivatedFinger==2):
        if(middleFinger):PauseGlove();
    elif(gloveActivatedFinger==3):
        if(ringFinger):PauseGlove();
    elif(gloveActivatedFinger==4):
        if(littleFinger):PauseGlove();


    #thumb=True
    if(gloveActivated):
        if(thumb): eval(SplitMessage[0]+'()')
        if(indexFinger): eval(SplitMessage[1]+'()')
        if(middleFinger): eval(SplitMessage[2]+'()')
        if(ringFinger): eval(SplitMessage[3]+'()')
        if(littleFinger): eval(SplitMessage[4]+'()')