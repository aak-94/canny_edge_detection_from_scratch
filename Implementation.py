# -*- coding: utf-8 -*-
"""
Created on Tue May 25 18:43:28 2021

@author: Akshay Khot
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv2
from cannyDetector_class import cannyEdgeDetector

#OpenCV uses BGR as its default colour order for images, matplotlib uses RGB

def loaddata():
    imgpath3= "./image.png"
    img3=cv2.imread(imgpath3,1)
    return img3

    
def canny_edge(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray2= gray.astype('int32')
    plt.imshow(gray,cmap='gray')
    plt.title("original")
    plt.show()
    detector = cannyEdgeDetector(gray2, gray, sigma=3, ksize=5,upper_threshold=0.2,lower_threshold=0.18)#lowthreshold=0.09, highthreshold=0.17)
    result_img = detector.Execute_canny()
    
    plt.imshow(result_img,cmap = 'gray')
    plt.title("final Result")
    plt.show()
    
    cv2.imshow('final',result_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    
def main():
    img=loaddata()
    canny_edge(img)
    print("main is implemented")
    
if __name__ == "__main__":
    main()