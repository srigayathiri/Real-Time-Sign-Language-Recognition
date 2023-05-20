import cv2
import htModule as htm
import numpy as np
import math
import time

# Create a VideoCapture object to read the video stream from the default camera
cap = cv2.VideoCapture(0)

# Create a HandDetector object to detect hands in each frame
detector =  htm.handDetector(maxHands=1)

# To make the image cropped to be in correct width and height
offset = 10

#Size of the white matrix or image
imgSize = 300

#Creating a folder to save the image
folder = "C:\\Users\\hp\\OneDrive\\Desktop\\Project\\Data\\Z"

#To have a track on number of images saved
counter=0

# Start an infinite loop to read and process each frame from the video stream
while True:
    # Read a frame from the video stream
    success,img = cap.read()

    img = cv2.flip(img, 1)
    
    # Detect hands in the current frame using the HandDetector object

    hands,imgLandmark = detector.findHands(img,draw=True)

    if hands:
        # Representing the first hand
        hand = hands[0]

        #This will give the coordinates along with the width and height from boundary box
        x,y,w,h = hand['bbox']

        #To create a white matrix (uint8 represents unsigned int) multiply with 255 to get white image else it produce black
        imgWhite = np.ones((imgSize,imgSize,3),np.uint8)*255

        #To get the cropped image
        imgCrop = imgLandmark[y-offset:y+h+offset,x-offset:x+w+offset]

        #To place the cropped image on white bg

        imgCropShape = imgCrop.shape

        #To place the image center on white matrix 

        aspectRatio = h/w

        #If the height greater than the width then make the height to imgSize and stretch the width to wCal
        if aspectRatio > 1:
            k= imgSize / h
            wCal = math.ceil(k * w)
            if imgCrop.size>0:
                imgResize = cv2.resize(imgCrop,(wCal,imgSize))
            else:
                continue
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal) / 2)

            #The height remain the same so we are using : for height
            imgWhite[:,wGap:wCal+wGap] = imgResize

        #If the width greater than the height then make the width to imgSize and stretch the height to hCal
        else:
            k= imgSize / w
            hCal = math.ceil(k * h)
            if imgCrop.size>0:
                imgResize = cv2.resize(imgCrop,(imgSize,hCal))
            else:
                continue
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal) / 2)

            #The width remain the same so we are using : for width
            imgWhite[hGap:hCal+hGap, :] = imgResize


        cv2.imshow("Imagecrop",imgCrop)
        cv2.imshow("ImageWhite",imgWhite)

    
    # Display the processed frame in a window named "Image"
    cv2.imshow("Image",img)
    
    # Wait for a key press event 
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter+=1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg',imgWhite)
        print(counter)
        

# Release the resources used by the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()