# AgriScan
## A-Level Computer Science coursework - Agricultural damage scanner 

### Overview 
AgriScan is a crop damage analysis tool built for farmers to locate areas of crop damage and calculate the area of damage. This project made up the coursework element of my A-Level in Computer Science.


![Alt text](sampleImage.jpg?raw=true "Title")
![Alt text](result_2020_11_25_13_46_16.jpg?raw=true "Title")


### How it works
AgriScan requires the image uploaded to have a distinct rectangular white marker (a beedsheet) visible in the frame. A Hue Saturation Value (HSV) subtraction for a range of white values is made to locate the marker within the image. The area of the marker is known, so the number of pixels that make up the marker in the image (found from the colour subtraction) can be used to work out the number of pixels that represent 1m^2. The user can then use the trackbar to manipulate the HSV values of the mask to fit the area of damage seen on the image. The number of pixels in the damage mask is then compaired to the number of pixels in the white marker to calculate the total area of damage. 

### How to use
run AgriScan.py. Click on the 'select image form files' button to open up file explorer. Select a .jpg or .png image file (make sure it contains the white marker). Once uploaded successfully, the image can be seen in the 'result' window. A 'help' window is also visible with further instructions (This can be closed by pressing the red exit button in the top right hand corner). The 'marker' window and trackbar will also be visible. 

use the trackbar sliders to manipulate the damage area until the blue contour fills only the damaged areas on the image. Refine the result by compairing the blue damage area with the white areas on the 'mask' window. Try to elimiate as much white noise as possible before saving. 

To save results once processed, press the ```Spacebar``` on the keyboard to save the results to the /results folder. Progress will not be lost and the image will be saved automatically with a unique timestamp in the filename.

To exit the damage tools, pres the ```Esc``` key on the keyboard. 

### Requirements 
Numpy,
OpenCV
```
pip install numpy 
pip install opencv-python
```

### Known problems 
Trackbar low and high values overlap,
filepaths are Windows specific (e.g. C:\Path\To\File... instead of C:/Path/To/File...)

### Tested on 
Windows 10, 
Python 3.7,
Numpy 1.17.3,
OpenCV 4.1.1,
