import cv2 
import numpy as np 
import imutils
from PIL import Image

widthImg=540
heightImg =640
capture = cv2.VideoCapture(0)
capture.set (3, 640)
capture.set (4, 480)

def preProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2) #2 passes of Dilation, thicker
    imgThresh = cv2.erode(imgDial,kernel,iterations=1) #1 pass of Erosion, thinner
    return imgThresh

def getContours(img):
    contours = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    maxArea = 0
    biggest = np.array([])
    for cont in contours:
        area = cv2.contourArea(cont)
        if area>5000:
            cv2.drawContours(imgContour,cont,-1,(255,0,0),3)   
            perimeter = cv2.arcLength(cont,True)
            approx = cv2.approxPolyDP(cont, .03*perimeter, True)
            if len(approx) ==4 and area>maxArea:
                biggest = approx
                maxArea=area          
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest

def reorder (myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    diff = np.diff(myPoints,axis=1)
    myPointsNew[0] = myPoints[np.argmin(add)] #smallest point when added
    myPointsNew[3] = myPoints[np.argmax(add)] #largest point when added
    myPointsNew[1]= myPoints[np.argmin(diff)] # smallest point when height-width
    myPointsNew[2] = myPoints[np.argmax(diff)] # largest point when height-width
    return myPointsNew

def getWarp(img,biggest):
    biggest =reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    
    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped,(widthImg,heightImg))
 
    return imgCropped

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

    
success,vid = capture.read() 
print("Press s to save image")
print("Press x to close program")
while success:
    img = cv2.resize(vid,(widthImg,heightImg))
    imgContour = img.copy()
 
    imgThres = preProcessing(img)
    biggest = getContours(imgThres)
    if biggest.size !=0:
        imgWarped=getWarp(img,biggest)
        imageArray = ([imgContour, imgWarped])
        cv2.imshow("ImageWarped", imgWarped)
    else:
        imageArray = ([imgContour, img])
 
    stackedImages = stackImages(0.6,imageArray)
    cv2.imshow("WorkFlow", stackedImages)
    
    if cv2.waitKey(16) & 0xFF==ord('x'):
        break
    if cv2.waitKey(16) & 0xFF==ord('s'):
        cv2.imwrite("ScannedImage.jpg",imgWarped)
        image1 = Image.open("ScannedImage.jpg")
        pdf = image1.convert("RGB")
        pdf.save("Scan.pdf")
        break
    if cv2.getWindowProperty("ImageWarped", cv2.WND_PROP_VISIBLE)<1:
        break
    if cv2.getWindowProperty("WorkFlow", cv2.WND_PROP_VISIBLE) <1:
        break
    success, vid = capture.read()

capture.release()
cv2.destroyAllWindows()