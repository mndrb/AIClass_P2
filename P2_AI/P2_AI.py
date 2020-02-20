import cv2
import numpy as np
import os
import DetectChars
import DetectPlates
import PossiblePlate

RED = (0.0, 0.0, 255.0)
imageid=0
read=True

def main():
    global imageid 
    imageid+=1
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()    
    if blnKNNTrainingSuccessful == False:                              
        print("Image Not Found") 
        return                              
    if(read==False):imgOriginalScene  = cv2.imread("LicPlateImages/"+str(imageid)+".jpg")
    else:imgOriginalScene  = cv2.imread("LicPlateImages2/"+str(imageid)+".png")
    if imgOriginalScene is None:                           
      print("\nerror: image not read from file \n\n")
      os.system("pause") 
      return 
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)
    cv2.imshow("imgOriginalScene", imgOriginalScene)   
    if len(listOfPossiblePlates) == 0:                   
        print("\nno license plates were detected\n") 
    else:                                          
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
        licPlate = listOfPossiblePlates[0]
        if len(licPlate.strChars) == 0:
            print("\nno characters were detected\n\n") 
            return
        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)   
        if(read):
            print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        print("----------------------------------------")
        cv2.imshow("imgOriginalScene", imgOriginalScene)              
        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)     
        cv2.waitKey(33)
    return

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)          
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), RED, 2)

if __name__ == "__main__":
   main()
   while(True):
    print("Next Image?(Press Y To Continue)")
    inp = input()
    if(str(inp)=="y" or str(inp)=="Y"):
     cv2.destroyAllWindows()
     main()
    else:
     break




















