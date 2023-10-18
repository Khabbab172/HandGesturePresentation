import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# variables
width , height = 1280 , 720
folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0) ;
cap.set(3 , width)
cap.set(4, height)

# Get the list of presentation images
pathImages =sorted( os.listdir(folderPath) , key=len )
print(pathImages)

# Variables
imgNumber = 0
hs , ws = int(120*1) , int(213*1)
gestureThreshold = 300

buttonPressed = False
buttonCounter = 0
buttonDelay = 20

annotations = [[]]
annotationsNumber = -1
annotationStart = False


# Hand Detector
detector = HandDetector(detectionCon=0.8 , maxHands=1 )

while True:

    # import images 
    success , img = cap.read()
    img = cv2.flip(img , 1 )
    pathFullImage = os.path.join(folderPath ,pathImages[imgNumber]) 
    imgCurrent = cv2.imread(pathFullImage)

    hands , img = detector.findHands(img , flipType=False)
    cv2.line(img , ( 0 , gestureThreshold ) , (width , gestureThreshold ) , (0 , 255 , 0 ) , 10) 

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx , cy = hand['center']
        lmList =  hand['lmList']
        indexFinger = lmList[8][0] , lmList[8][1]
        xVal = int(np.interp(lmList[8][0], [width//2 , w] , [0 , width]))
        yVal = int(np.interp(lmList[8][1] , [150 , height - 150 ] , [0 , height]))
        indexFinger = xVal , yVal

        if cy <= gestureThreshold : # if hand is above line
            print(fingers)
            # gesture - Left
            if fingers == [0 , 0 , 0 , 0 , 0 ]:
                print("Left")
                if imgNumber > 0:
                    buttonPressed = True
                    imgNumber -= 1
                    annotations = [[]]
                    annotationsNumber = -1
                    annotationStart = False
                    
            # gesture - Right
            if fingers == [1 , 0 , 0 , 0 , 1 ]:
                print("Right")
                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    imgNumber += 1
                    annotations = [[]]
                    annotationsNumber = -1
                    annotationStart = False
                    
        # gesture - show pointer
        if fingers == [1 , 1 , 1 , 0 , 0 ]:
            cv2.circle(imgCurrent ,indexFinger , 12 , (0 , 0 , 255) , cv2.FILLED)
            annotationStart = False

        # gesture - Draw Pointer
        if fingers == [1 , 1 , 0 , 0 , 0 ]:
            if annotationStart is False:
                annotationStart = True
                annotationsNumber += 1
                annotations.append([])
                print(annotationsNumber)
            cv2.circle(imgCurrent ,indexFinger , 12 , (0 , 0 , 255) , cv2.FILLED)
            annotations[annotationsNumber].append(indexFinger)
        else:
            annotationStart = False
            
        # gesture - erase
        if fingers == [1 , 1 , 1 , 1 , 0 ]:
            if annotations:
                annotations.pop(-1)
                annotationsNumber -= 1
                buttonPressed = True
                
                
            
    # button pressed itrations             
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay :
            buttonCounter = 0
            buttonPressed = False

    # drawing   
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent , annotations[i][j -1] , annotations[i][j] ,(0 , 0 , 200 ) ,12 )
        
    # Adding webcam Image on the slides
    imgSmall = cv2.resize( img , (ws , hs ))
    h , w , _ = imgCurrent.shape
    imgCurrent[0:hs , w-ws:w] = imgSmall
    
    cv2.imshow("Image" , img )
    cv2.imshow("Slides" , imgCurrent )

    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break





