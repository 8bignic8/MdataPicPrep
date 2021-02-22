#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse, os
import cv2
import numpy as np
import imageio
import time


# In[2]:


def savePic(picture,fileName,extention,outPath):
    outPath = outPath+fileName+'.'+extention # combines the path with the name and extention of the file
    try:
        #imageio.imwrite(outPath,picture,format=extention)# old way
        cv2.imwrite(outPath,picture)#saves Pictures 
        print(outPath+' <==== Writing')
    except:
        print('Failed while saving picture: '+fileName+' to '+ outPath+' sorry :(') #writes an error
        print('--------------------')


# In[3]:


def readPicture(picturepath):
    #  open ImageObject
    img = cv2.imread(picturepath, cv2.IMREAD_UNCHANGED)#cv2.IMREAD_UNCHANGED is important that the output is (x,y,ChannelRGB)
    #print(img.shape)
    #alternative
    #img=imageio.imread(picturepath) #liest Bild von picturepath
    return(img)


# In[4]:


def RGBtoYUV(img): #changeing the img picture from RGB- to YUV-Color space
    pictureYUV = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    return pictureYUV


# In[5]:


print('This program creates Singel YUV or RGB pictures, or splits the pictures in 3 single cromagan pictures')
path = input('Path to pictures who should be converted defaut: ./hdrInput/: ') or './hdrInput/'
if not os.path.exists(path):
            os.mkdir(path)
inputextention = input('What fileextention do the to converting pictures have? [default: png]') or 'png'
allFilesInDir = sum(1 for f in os.listdir(path) if f.endswith('.'+inputextention)) #summ all ending with extention
print('There are: '+str(allFilesInDir)+' files with the extention '+inputextention+' in the folder')
toconvert = input('How many do you want to convert? default: 2') or '2'
outputextention = input('Please type in the output format default: png ') or 'png'
singleP = input('Do you want to split the pictures in single color channel 3*(x,y,1) pictures? deflaut: no (x,y,3)') or 'no'
toYUV = input('Do you want to convert the output to YUV color space? deflaut: no(RGB output)') or 'no'


# In[6]:


####This program creates Singel YUV or RGB pictures or splits the pictures in 3 single cromagan pictures
start_time = time.time() #start the timeing of the Prgramm
i = 1 # start at the 1th element in the file system
while (i <= int(toconvert)): # for all the inputdata in the folder do
    name = os.listdir(path)[i] #finding the name at the current position and save it
    picpath = path + name #combining filename and path
    print(picpath+' ====> Reading') # prints the path and filename
    pic = readPicture(picpath) # imports the picture and saves it in pic as matrix
    namePic = (name.split('.')[0]) #cuts out the extention
    if (outputextention == 'png'):#if it is png save it in the PNG folder
        outputpath = './sdrOut/'
        if(inputextention == 'hdr' or 'exr'):
            pic = pic*((2 ** 10)-1) #multiplys it by the 10bit to geht the pixel depth
    if (outputextention != 'png'):# save everyting else here
        outputpath = './hdrOut/'
    if(toYUV != 'no'): #if the user wants to convert the output in YUV
        pic = RGBtoYUV(pic)#converts the picture to YUV
    if(singleP != 'no'):
        print('waring, Lossy RGB to YU-V conversion')
        #print(pic.shape)
        u = (pic[:,:,2]) #orders the color channels to the right output value
        v = (pic[:,:,1]) 
        y = (pic[:,:,0])
        if (toYUV != 'no'):
            spaceIndi = 'u','v','y' #orders the Name to the right place
        if (toYUV == 'no'):
            spaceIndi = 'b','g','r'
        print('ALl pictures will appear black')
        savePic(u,(str(i)+'-'+spaceIndi[0]+'_'+namePic),outputextention,outputpath)#saves final singel color channel Picture
        savePic(v,(str(i)+'-'+spaceIndi[1]+'_'+namePic),outputextention,outputpath)#saves final singel color channel Picture
        savePic(y,(str(i)+'-'+spaceIndi[2]+'_'+namePic),outputextention,outputpath)#saves final singel color channel Picture
    if(singleP == 'no'):#just converts the pictures
        savePic(pic,(str(i)+namePic),outputextention,outputpath)#saves final U singel channel Picture
    i = i + 1
print('It took: '+str((time.time() - start_time)/60)+' Minutes to finish') 
print('------Done------:)')


# In[ ]:




