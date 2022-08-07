
import cv2

def nadjiRuku(slikaRuke,ruke):
    imgRGB = cv2.cvtColor(slikaRuke, cv2.COLOR_BGR2RGB)
    return ruke.process(imgRGB)
