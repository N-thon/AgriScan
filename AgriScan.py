#################################################################
# AgriScan                                                      #
# A-Level Computer Science project:                             #
#     Analyse images of crop fields and locate areas of damage  #
#     and calculate the size of the damage area. Uses OpenCV    #
#     and Numpy for image manipulation and TKinter for some GUI #
#     elements.                                                 #
#################################################################

# imports 
import tkinter as tk                
import tkinter.messagebox           
from tkinter import filedialog

import datetime
import cv2                          
import numpy as np                  
import os  

class AgriScan(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.screenHeight = self.winfo_screenheight()
        self.screenWidth =  self.winfo_screenwidth()
        self.font = ("Helvetica", 16)
        parent.title("AgriScan")
        parent["bg"] = "#228822"
        geo = str(self.screenWidth//2) + "x" + str(self.screenHeight//2) + "+0+0"
        parent.geometry(geo)

        welcomeWidget = tk.Label(parent, text = "Welcome to AgriScan", bg=parent["bg"], activebackground=parent["bg"], font=self.font, width=self.screenWidth//20, height=self.screenHeight//100).grid(row=1, column=0)
        choseImgWidget = tk.Button(parent, command=lambda:self.findImage(), text = "Select image from files",bg=parent["bg"], activebackground=parent["bg"], font=self.font, width=self.screenWidth//80, height=self.screenHeight//200).grid(row=2, column=0)

    def findDamage(self):
        """
            manipulates a copy of the image to locate the areas of
            damage using user Hue, Saturation and Value inputs and
            calculates the total area of damage. The damage area is
            displayed in an OpenCV window and updated by an OpenCV
            trackbar. The resulting image can be saved by pressing
            "spacebar" or abandoned by pressing "esc".
        """

        # copy image
        img = self.image.copy()

        # create and position the OpenCV windows
        cv2.namedWindow("img")
        cv2.moveWindow("img",0,0)
        cv2.resizeWindow("img",self.screenWidth//3, self.screenHeight//2)

        cv2.namedWindow("result")
        cv2.moveWindow("result",self.screenWidth//3,0)
        cv2.resizeWindow("result",self.screenWidth//3, self.screenHeight//2)

        cv2.namedWindow("mask")
        cv2.moveWindow("mask",2*(self.screenWidth//3),0)
        cv2.resizeWindow("mask",self.screenWidth//3, self.screenHeight//2)

        cv2.namedWindow("Help")
        cv2.moveWindow("Help", self.screenWidth//10, self.screenHeight//10)
        cv2.resizeWindow("Help",self.screenWidth//3, self.screenHeight//2)
        path = os.getcwd() + "\help.png"
        helpImg = cv2.imread(path)
        cv2.imshow("Help",helpImg)

        # empty function "nothing" has to be declared as createTrackbar() accepts 5 parameters
        def nothing(x):
            pass
        # create trackbar names, ranges and starting positions
        cv2.createTrackbar("Min-Hue", "img", 0, 180, nothing)
        cv2.createTrackbar("Min-sat", "img", 0, 255, nothing)
        cv2.createTrackbar("Min-Val", "img", 0, 255, nothing)
        cv2.createTrackbar("Max-Hue", "img", 180, 180, nothing)
        cv2.createTrackbar("Max-Sat", "img", 255, 255, nothing)
        cv2.createTrackbar("Max-Val", "img", 255, 255, nothing)
        cv2.createTrackbar("Blur","img", 0, 50, nothing)

        # the image is continually updated during editing
        while True:
            img = self.image
            dim = (self.screenWidth//3, self.screenHeight//2)
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

            # gets the HSV values from the trackbar 
            minHue = cv2.getTrackbarPos("Min-Hue","img")
            minSat = cv2.getTrackbarPos("Min-Sat","img")
            minVal = cv2.getTrackbarPos("Min-Val","img")
            maxHue = cv2.getTrackbarPos("Max-Hue","img")
            maxSat = cv2.getTrackbarPos("Max-Sat","img")
            maxVal = cv2.getTrackbarPos("Max-Val","img")
            medBlur = cv2.getTrackbarPos("Blur","img")
            # cv2.medianBlur only accepts odd values
            medBlur = ((1 + medBlur)//2)*2 + 1

            # defines HSV ranges for damage area using trackbar positions
            lowerDamage = np.array([minHue,minSat,minVal])
            upperDamage = np.array([maxHue,maxSat,maxVal])

            # applies the colour subtraction to the image
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lowerDamage, upperDamage)
            median = cv2.medianBlur(mask, medBlur)
            cv2.imshow("mask", mask)
            
            # counts the number of pixels enclosed within the contours of the marker and calculates the damage area
            damagePixel = np.count_nonzero(median)
            damageArea = round(((damagePixel / self.markerPixelCount) * self.markerArea),2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, "Damage = {}m^2".format(damageArea), (10,30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # creates an overlay to make the contours transparrent on the resulting image
            overlay = img.copy()
            
            # draws the contours of the damaged area on the image
            contours,_ = cv2.findContours(median,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                cv2.fillPoly(img, pts =[contour], color=(255,0,0))

            # applies the contours over the original image with a transparancy of alpha
            alpha = 0.6 
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            cv2.imshow("result",img)

            # loop continues until "esc" or "spacebar" are pressed, abandoning the edditing and saving the image respectivly
            key = cv2.waitKey(1)
            if key == 32:
                # add HSV ranges to saved image
                hueStr = " Min-Hue = " + str(minHue) + ", Max-Hue = " + str(maxHue)
                satStr = " Min-Sat = " + str(minSat) + ", Max-Sat = "+ str(maxSat)
                valStr = " Min-Val = " + str(minVal) + ", Max-Val = " + str(maxVal)
                cv2.putText(img, "{}".format(hueStr), (10,75), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, "{}".format(satStr), (10,125), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, "{}".format(valStr), (10,200), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                try:
                    # filedialog save doesn't seem to bee working. Currently saving using cv2.imwrite with a timestampped name in a results folder 
                    #img = filedialog.asksaveasfilename(filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
                    path = str(os.path.dirname(__file__))
                    file = '\\results\\result_{}.jpg'.format(str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
                    path += file
                    cv2.imwrite(path,img)
                except:
                    tkinter.messagebox.showinfo("Error Message", "Unable to save file!")
            if key == 27:
                break
        cv2.destroyAllWindows()   



    def findMarker(self):
        """
            Manipulates a copy of the image to find the white marker in the image
            then calculates the number of pixels that make up the marker. Achieves
            this by doing a colour subtraction for a range of HSV(Hue, Sauration,
            Value) in the white spectrum and finding the largest white region in the
            image. 
        """

        img = self.image.copy()
        
        # image is changed from Blue, Green and Red to Hue Saturation and Value(HSV) for the colour subtraction
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # defines HSV ranges for white
        lowerWhite = np.array([0,0,0])
        upperWhite = np.array([0,0,255])
        sought = [255,0,255]

        # applies the colour subtraction to the image
        mask = cv2.inRange(hsv, lowerWhite, upperWhite)
        
        # finds the contours of the colour subtraction boundaries
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # finds the largest contour (the white marker) and draws a rectangle around it
        for contour in contours:
            c = max(contours, key = cv2.contourArea)
            #print(c)
            
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),-1)
            #else:
            #    tkinter.messagebox.showinfo("Error Message", "Marker not found!")
            #    root.destroy
            #    return

        # counts the number of pixels enclosed within the contours of the marker
        self.markerPixelCount = np.count_nonzero(np.all(img == sought, axis = 2))
        self.markerArea = 2.5

        # finds damage areas
        self.findDamage()



    def findImage(self):
        """
            Opens file explorer using "filedialog" for the user to
            select an image file to process. This image is then checked,
            resized and opened as an OpenCV object using "imread"
        """
        
        # opens documents so the user can select a file
        filepath = filedialog.askopenfilename()

        # checks that the selected file is a .jpg or .png file
        if len(filepath) > 0:
            check = filepath[-4:]
            if check.lower() != ".jpg" and check.lower() != ".png":
                tkinter.messagebox.showinfo("Error Message", "Please insure that you load a .png or .jpg file!")
                root.destroy
                return  
        else:
            tkinter.messagebox.showinfo("Error Message", "No file found!")
            root.destroy
            return

        # attempts to open the file as an OpenCV object called self.image
        try:
            self.image = cv2.imread(filepath)
        except:
            tkinter.messagebox.showinfo("Error Message", "OpenCV was unable to read the file!")
            root.destroy
            return 
        
        # resize image
        dim = (self.screenWidth//3, self.screenHeight//2)
        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)

        # locates the marker     
        self.findMarker()



if __name__ == "__main__":
    root = tk.Tk()
    AgriScan(root)
    root.mainloop()
