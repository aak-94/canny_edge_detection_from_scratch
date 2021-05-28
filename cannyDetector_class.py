# -*- coding: utf-8 -*-
"""
Created on Wed May 26 14:47:23 2021

@author: Akshay Khot
"""
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

class cannyEdgeDetector:
    def __init__(self,img,img2,sigma,ksize,upper_threshold,lower_threshold):
        self.img = img                       # img as int32
        self.img2 = img2                     # input image
        self.sigma = sigma                   # guassian sigma vlaue
        self.ksize = ksize                   # Kernel window size
        self.Uthreshold =upper_threshold     # Higher threshold limit
        self.Lthreshold = lower_threshold    # Lower threshold limit

    
    def gaussion_blurr(self):
        size = int(self.ksize) // 2
        x, y = np.mgrid[-size:size+1, -size:size+1]
        normal = 1 / (2.0 * np.pi * self.sigma**2)
        g_filter =  np.exp(-((x**2 + y**2) / (2.0*self.sigma**2))) * normal
        smoothened_img= ndimage.filters.convolve(self.img, g_filter)
        smoothened_img2= ndimage.filters.convolve(self.img2, g_filter)
        plt.imshow(smoothened_img,cmap = 'gray')
        plt.title("Gaussian"), plt.xticks([]),plt.yticks([])
        plt.show()
        return (smoothened_img,smoothened_img2)
    
    def gradient_and_direction(self,smoothened_img,smoothened_img2):
        #using soble filters to find gradient in x and y directions
        Kx_filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
        Ky_filter = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
        
        I_x = ndimage.filters.convolve(smoothened_img, Kx_filter)
        I_y = ndimage.filters.convolve(smoothened_img, Ky_filter)
        gradient = np.hypot(I_x,I_y)            
        gradient =gradient/gradient.max()          #This gradient is an image
        theta =np.degrees(np.arctan2(I_y,I_x))
        
        I_x2 = ndimage.filters.convolve(smoothened_img2, Kx_filter)
        I_y2 = ndimage.filters.convolve(smoothened_img2, Ky_filter)
        gradient2 = np.hypot(I_x2,I_y2)          
        gradient2 =gradient2/gradient2.max()*255
        gradient2= gradient2.astype('uint8')
        
        plt.subplot(1,2,1)
        plt.imshow(gradient,cmap = 'gray')
        plt.title("soble x & Y as int32"), plt.xticks([]),plt.yticks([])
        plt.subplot(1,2,2)
        plt.imshow(gradient2,cmap = 'gray')
        plt.title("soble x & Y of uint8"), plt.xticks([]),plt.yticks([])
        plt.show()
        
        return (gradient,theta)
    
    def Non_max_suppresion(self,gradient,theta):    
        #The algorithm goes through all the points on the gradient intensity matrix
        #and finds the pixels with the maximum value in the edge directions. 
        img= gradient
        H,W = img.shape
        theta[theta<0]+=180   #to convert negative angles
        #range is decided considering the border of one pixle
        for i in range(1,H-1): 
            for j in range(1,W-1):
                    #Following if conditions would define the two necesary intensities q,r adjecent to the current pixle img[i,j]
                    #q is the forward pixle and r is the rear pixle in the direction theta
                    #angle 0
                    if (0 <= theta[i,j] < 22.5) or (157.5 <= theta[i,j] <= 180):
                        q = img[i, j+1]
                        r = img[i, j-1]
                    #angle 45
                    elif (22.5 <= theta[i,j] < 67.5):
                        q = img[i-1, j+1]
                        r = img[i+1, j-1]
                    #angle 90
                    elif (67.5 <= theta[i,j] < 112.5):
                        q = img[i-1, j]
                        r = img[i+1, j]
                    #angle 135
                    elif (112.5 <= theta[i,j] < 157.5):
                        q = img[i-1, j-1]
                        r = img[i+1, j+1]
                        
                    if (img[i,j]>=q and img[i,j]>=r):
                        img[i,j]=img[i,j]
                    else:
                        img[i,j]=0
        thin_edge =img
        plt.figure()
        plt.imshow(thin_edge,cmap = 'gray')
        plt.title("thin_edge"), plt.xticks([]),plt.yticks([])
        plt.show()
        return thin_edge
    
    def double_thresholding_and_hysteresis(self,thin_edge):
        U_th = self.Uthreshold
        L_th = self.Lthreshold
        H,W = thin_edge.shape
        #range is decided considering the border of one pixle
        for i in range(1,H-1):
            for j in range(1,W-1):
                if (thin_edge[i,j] > U_th):
                    thin_edge[i,j]=255
                elif(thin_edge[i,j] < L_th):
                    thin_edge[i,j] = 0
                else:
                    if ((thin_edge[i+1, j-1] > U_th) or (thin_edge[i+1, j] > U_th) or (thin_edge[i+1, j+1]> U_th)
                            or (thin_edge[i, j-1] > U_th) or (thin_edge[i, j+1] > U_th)
                            or (thin_edge[i-1, j-1]> U_th) or (thin_edge[i-1, j] > U_th) or (thin_edge[i-1, j+1] > U_th)):
                        thin_edge[i,j]=255
        canny_edge = thin_edge
        return canny_edge
    
    def Execute_canny(self):
        smoothened_img,smoothened_img2 = self.gaussion_blurr()
        gradient,theta = self.gradient_and_direction(smoothened_img,smoothened_img2)
        thin_edge = self.Non_max_suppresion(gradient,theta)
        canny_edge =self.double_thresholding_and_hysteresis(thin_edge)
        return canny_edge
        
        
        
                    
            