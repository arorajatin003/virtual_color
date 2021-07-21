# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 16:52:34 2021

@author: user
"""

import cv2
import numpy as np


video = cv2.VideoCapture(0)
video.set(3,640)
video.set(4,480)
video.set(10,150)

myColor = [[109,34,34,132,179,179],
           [0,159,159,14,240,240],
           [69,70,70,82,253,253],
           ]

myColorValues = [[255, 0, 0],           
                 [0, 0, 255], 
                 [0, 255, 0],            
                 ] 
  
 
myPoints = []   

def findColor(img,myColor,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = [] 
       
    for color in myColor:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mack = cv2.inRange(imgHSV,lower,upper)
        x,y = getCorner(mack)
        cv2.circle(imgResult, (x,y), 15, 
                   myColorValues[count], cv2.FILLED) 
        if x != 0 and y != 0: 
            newPoints.append([x,y,count]) 
        count += 1
    return newPoints 

def getCorner(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>250:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y
    
def drawOnCanvas(myPoints, myColorValues): 
    for point in myPoints: 
        cv2.circle(imgResult, (point[0], point[1]), 
                   10, myColorValues[point[2]], cv2.FILLED) 
    
while True:
    success, img = video.read() 
    imgResult = img.copy() 
  
   
    newPoints = findColor(img, myColor, myColorValues) 
    if len(newPoints)!= 0: 
        for newP in newPoints: 
            myPoints.append(newP) 
    if len(myPoints)!= 0: 
  
        
        drawOnCanvas(myPoints, myColorValues) 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Result", imgResult) 

video.release()
cv2.destroyAllWindows()



