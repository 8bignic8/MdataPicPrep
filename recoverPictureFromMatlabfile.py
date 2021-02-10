#!/usr/bin/env python
# coding: utf-8

# In[1]:


import h5py as h5
import hdf5storage
import numpy as np
import imageio
import mat73
import os
import cv2
import time
import argparse


# In[2]:


def savePic(picture,fileName,extention,outPath): #saves the given array as a pictures to the given output path
    outPath = outPath+fileName+'.'+extention
    print(outPath)
    try:
        #old
        #imageio.imwrite(outPath,picture,format=extention)#extention'')#save the Data (path with name and file extention,PictureMatrix,format)
        #new
        cv2.imwrite(outPath,picture)
    except:
        print('Failed while saving picture: '+fileName+' to '+ outPath+' sorry :(')
        print('--------------------')


# In[3]:


def YUVtoRGB(img):
    pictureYUV = cv2.cvtColor(img, cv2.COLOR_YUV2RGB, cv2.IMREAD_UNCHANGED) #uses the CV2 method to convert the color space from YU-V to RGB
    return pictureYUV


# In[4]:


def convert(img, target_type_min, target_type_max): # converts the input array to target bounderys given
    imin = img.min()
    imax = img.max()
    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b)
    return new_img


# In[25]:


# Reads a matlab file and saves the pictures in the .png or .hdr Format
def recoverpic(pathToFile):
    
#input part
    mat = hdf5storage.loadmat(pathToFile) #loads the matlab file
    key = mat.keys() #reads the mat key
    key = str(key).split('\'')[1] # saves the keyname(HDR,SDR) in key
    allPictures = int((mat[key][0,0,0,:]).shape[0]) # reads the amount of pictures in the .mat file
    sdrOutPath = input('Where should the SDR data be saved?[default: ./sdrOut/ ]: ') or './sdrOut/'
    if not os.path.exists(sdrOutPath):
        os.mkdir(sdrOutPath)
    hdrOutPath = input('Where should the HDR data be saved?[default: ./hdrOut/ ]: ') or './hdrOut/'
    if not os.path.exists(hdrOutPath):
        os.mkdir(hdrOutPath)    
    numberOfP = input('How many pictures from: '+str(allPictures)+' should be saved?[default: 23 ]: ') or '23'#str(allPictures-1)
    numberOfP = int(numberOfP) #forms the input(string) into an integer 
    onePic = input('Do you want it split in single Y.png U.png V.png?  default: no') or 'no'
    if (onePic == 'no'):
        fileName = input('what should be the name of the outputfiles? default: out_ ') or 'out_'
    toPictures = allPictures - numberOfP
    print(key)
    print(str(key).split('_')[0])
#=======Main program start
    if (key.split('_')[0] == 'HDR'):
        print('HDR pictures found in matlab file')
        if (onePic != 'no'):
            print('the single PNG pictures will be black but contain the Information if you put them together')
        while (toPictures <= int(allPictures)-1):
            picture = (mat[key][:,:,:,toPictures])#.astype(np.uint16) # create an array with the right size
            print('Writing HDR picture to: ')
            i = 0
            if (onePic == 'no'):
                #picture = picture / ((2 ** 10)-1)
                k = 'HDR_'+fileName+str(toPictures)
                savePic(picture,k,'hdr',hdrOutPath)
            if (onePic != 'no'):
                while(i<=2):
                    if(i==1):
                        outName = str(toPictures)+'-u_pred'
                    if(i==0):
                        outName = str(toPictures)+'-y_pred'
                    if(i==2):
                        outName = str(toPictures)+'-v_pred'
                    savePic((picture[:,:,i]),outName,'png',hdrOutPath) #it saves as a 16bit .png with one single color channel
                    i = i + 1
            toPictures = toPictures+1
    print('finished writing hdr pictures to: ' + hdrOutPath)
    
    if (key.split('_')[0] == 'SDR'):
        print('SDR pictures found in matlab file')
        if (onePic != 'no'):
            print('the single PNG pictures will be black but contain all the information, just put them together')
        while (toPictures <= allPictures-1):
            picture = mat[key][:,:,:,toPictures].astype(np.uint8)
            i = 0
            print('Writing PNG picture to: ')
            if (onePic == 'no'):
                k = 'SDR_'+fileName+str(toPictures)
                savePic(picture,k,'png',sdrOutPath)
            if (onePic != 'no'):
                while(i<=2):
                    if(i==2):
                        outName = str(toPictures)+'-v_pred'
                    if(i==1):
                        outName = str(toPictures)+'-u_pred'
                    if(i==0):
                        outName = str(toPictures)+'-y_pred'
                    savePic((picture[:,:,i]),outName,'png',sdrOutPath) #it saves as a 8bit .png with one single color channel
                    i = i + 1
            toPictures = toPictures+1
        print('finished writing sdr pictures to: ' + sdrOutPath)      


# In[29]:


start_time = time.time()
print('Important: This is a program that recovers pictures saved as a .mat file via uint8 or uint16 format and SDR/ HDR label.')
try:
    pathtomat = input('Please insert the path to your .mat picture file default: ./matOut/') or './matOut/'
    name = input('Please type the name of the matlapfile default: HDR_data.mat') or 'HDR_data.mat'
    if not os.path.exists(pathtomat): #makes the drectory if it is not there
        os.mkdir(pathtomat)
    recov = pathtomat+name #puts together the filepath and name
    recoverpic(recov) #starts the recovery prozess
    
except: 
    print('decoding .mat failed')
print(str((time.time() - start_time)/60)+'Minutes') #outputs the time in minutes
print('------------------------- Done --------------------')


# In[ ]:




