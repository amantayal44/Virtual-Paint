import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0) 
cap.set(3,frameWidth) 
cap.set(4,frameHeight) 
cap.set(10,150) #brightness

# use color_picker to find (h_min,s_min,v_min,h_max,s_max,v_max)
ColorHSV = [[87,96,26,151,185,172],
            [156,123,74,179,207,119]]
ColorValues = [[237,63,24],
                 [237,24,159]]

allPoints = [] #(x,y,colorId)

def findColor(img,ColorHSV):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in ColorHSV:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        if x!= 0 and y!= 0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #retrive outer contours
    x,y,w,h =0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(allPoints):
    for point in allPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,ColorValues[point[2]],cv2.FILLED)
 
while True:
    success,img = cap.read() 
    if(not success): break
    imgResult = img.copy()
    newPoints = findColor(img,ColorHSV) 
    for newP in newPoints:
        allPoints.append(newP)
    drawOnCanvas(allPoints)        

    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'): #press q to break
        break  