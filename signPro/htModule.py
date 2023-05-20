import cv2
import mediapipe as mp
import numpy as np


class handDetector():

    #Basic parameter required for Hands in init function

    def __init__(self, mode=False, maxHands=2, detectionCon = 0.5, trackingCon = 0.5):

        #Crearing object that has its own variable and initially assigning with the value provided by the user

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon


        #Formality to be used in this model

        self.mpHands = mp.solutions.hands 
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackingCon)
        self.mp_drawing = mp.solutions.drawing_utils

        #To draw landmark in hands
        self.mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)

        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """

        img_w = np.empty(img.shape)
        img_w.fill(255)
       
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img_w, handLms,
                                               self.mpHands.HAND_CONNECTIONS,
                                               self.mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                               self.mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2))
                    cv2.rectangle(img_w, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(img_w, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        if draw:
            return allHands, img_w
        else:
            return allHands

    def findPosition(self,img, handNo=0, draw=True):

        #List containing the landmarks as coordinates

        lmlist = []

        if self.results.multi_hand_landmarks:

            #Getting landmark for specific hand

            myHand = self.results.multi_hand_landmarks[handNo]

            #To get id and landmark from the hand

            for id, lm in enumerate(myHand.landmark):

                #To get width height and channel 

                h, w, c = img.shape

                #To get the center coordinate as an integer

                cx,cy = int(lm.x * w), int(lm.y * h) 

                #Appending the id and coordinates of the particular hand

                lmlist.append([id, cx, cy])

                if draw:

                    cv2.circle(img, (cx,cy), 7, (255, 0, 255), cv2.FILLED)     

        return lmlist 


def main():

    #Creating object for capturing vdo

    cap = cv2.VideoCapture(0) 

    #Creating object for the class

    detector = handDetector()

    while True:

        #Reading vdo frame by frame

        success,img = cap.read()

        #After getting img calling findhands

        img = detector.findHands(img)

        lmlist = detector.findPosition(img)

        #Printing the values of list for the particular index(one of the 20 landmark)

        #if len(lmlist) !=0:

        #   print(lmlist[4])


        #Display the results

        cv2.imshow("Image",img) 

        #Close the window when exit clicked

        cv2.waitKey(1) 






if __name__=="__main__":
    main()