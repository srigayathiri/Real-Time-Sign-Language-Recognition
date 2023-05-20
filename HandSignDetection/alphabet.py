import cv2
import htModule as htm
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import os
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import enchant


# Create a VideoCapture object to read the video stream from the default camera
cap = cv2.VideoCapture(0)

# Create a HandDetector object to detect hands in each frame
detector =  htm.handDetector(maxHands=1)

global output,l,txt

# To make the image cropped to be in correct width and height
offset = 18

#Size of the white matrix or image
imgSize = 300

classifier = Classifier("C:\\Users\\hp\\OneDrive\\Desktop\\Project\\ModelPavi\\keras_model.h5","C:\\Users\\hp\\OneDrive\\Desktop\\Project\\ModelPavi\\labels.txt")
labels = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

# Create a tkinter GUI window
window = tk.Tk()
window.title("Sign Language To Text Conversion")
window.geometry("1300x700")
window['background']='#f04848'


panel = tk.Label(window)
panel.place(x=100, y=3, width=480, height=640)
panel['background']='#f04848'


# Load image
image1 = Image.open("C:\\Users\\hp\\OneDrive\\Desktop\\Project\\sign.jpg")

# Convert PIL image to Tkinter-compatible image
tk_image1 = ImageTk.PhotoImage(image1)

panel1 = tk.Label(window)
panel1.place(x=700, y=85, width=780, height=380)

panel1.tk_image1 = tk_image1
panel1.config(image=tk_image1)

l = tk.Label(window)
l.place(x=255, y=581)

ls = tk.Label(window)
ls.place(x=250, y=690)

T1 = tk.Label(window)
T1.place(x=10, y=580)
T1.config(text="Character :", font=("Helvetica", 25, "bold"),bg="#f04848")


l1 = tk.Label(window)
l1.place(x=10, y=690)
l1.config(text="Sentence :", font=("Helvetica", 25, "bold"),bg="#f04848")

#l2 = tk.Label(window)
#l2.place(x=10, y=720)
#l2.config(text="Suggestions :", font=("Helvetica", 25, "bold"),bg="#f04848")

def remove():
                ls.config(text="")
                store.clear()

buttonClear = tk.Button(window,text ="Clear",command=remove)
buttonClear.place(x=1205,y=630)
buttonClear.config(
    font=("Helvetica", 15,"bold"),  # Set the font
    fg="black",  # Set the text color  # Set the background color
    relief="solid",  # Set the border style
    padx=10,  # Set the horizontal padding
    pady=5,  # Set the vertical padding
    width=4,  # Set the width
    height=1  # Set the height
)

T = tk.Label(window)
T.place(x=470, y=10)
T.config(text="Sign Language To Text Conversion", font=("Helvetica", 25, "bold"),bg="#f04848")


# Start an infinite loop to read and process each frame from the video stream
store  = []

def update():


    global store
    
    global img, img_tk

    # Read a frame from the video stream
    success,img = cap.read()


    img = cv2.flip(img, 1)

    #Making the copy of the image to avoid drawing
    imgOutput = img.copy()

    
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
            imgResize = cv2.resize(imgCrop,(wCal,imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal) / 2)

            #The height remain the same so we are using : for height
            imgWhite[:,wGap:wCal+wGap] = imgResize

            prediction, index = classifier.getPrediction(imgWhite)

            #print(prediction,index)

        #If the width greater than the height then make the width to imgSize and stretch the height to hCal
        else:
            k= imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop,(imgSize,hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal) / 2)

            #The width remain the same so we are using : for width
            imgWhite[hGap:hCal+hGap, :] = imgResize

            prediction, index = classifier.getPrediction(imgWhite)

            #print(prediction,index)
        if prediction[index] >= 0.98:

            output = labels[index]

            txt = ""

            l.config(text=output, font=("Helvetica", 25, "bold"))
            l['background']='#f04848'

            def sentence():

                str1 = " "
                store.append(output)
                txt = str1.join(store)
                ls.config(text=txt, font=("Helvetica", 25, "bold"))
                ls['background']='#f04848'
                voice(txt)

                #to suggest words
                #def suggest_words(word):
                    #d = enchant.Dict("en_US")
                    #if not d.check(word):
                        #suggestions = d.suggest(word)[:4]
                        #return suggestions
                    #else:
                        #return " "

                #word = txt
                #suggestions = suggest_words(word)

                #lsug = tk.Label(window)
                #lsug.place(x=250, y=720)
                #txt = str1.join(store)
                #lsug.config(text=suggestions, font=("Helvetica", 25, "bold"))
                #lsug['background']='#f04848'

            def voice(txt):
                voice = pyttsx3.init()
                voice.say(txt)
                voice.runAndWait()


            buttonAdd = tk.Button(window,text ="Add",command=sentence)
            buttonAdd.place(x=1105,y=630)
            buttonAdd.config(
                font=("Helvetica", 15,"bold"),  # Set the font
                fg="black",  # Set the text color  # Set the background color
                relief="solid",  # Set the border style
                padx=10,  # Set the horizontal padding
                pady=5,  # Set the vertical padding
                width=4,  # Set the width
                height=1  # Set the height
            )


            buttonVoice = tk.Button(window,text ="Voice",command=voice)
            buttonVoice.place(x=1305,y=630)
            buttonVoice.config(
                font=("Helvetica", 15,"bold"),  # Set the font
                fg="black",  # Set the text color  # Set the background color
                relief="solid",  # Set the border style
                padx=10,  # Set the horizontal padding
                pady=5,  # Set the vertical padding
                width=4,  # Set the width
                height=1  # Set the height
            )



            cv2.putText(imgOutput,output,(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)


    imgOutput = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
    current_image = Image.fromarray(imgOutput)
    imgtk = ImageTk.PhotoImage(image=current_image)
    panel.imgtk = imgtk
    panel.config(image=imgtk)
    # Schedule the next update
    window.after(10, update)


update()

# Start the tkinter event loop
window.mainloop()

# Release the resources used by the VideoCapture object
cap.release()
cv2.destroyAllWindows()