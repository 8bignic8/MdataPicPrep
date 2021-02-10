#!/usr/bin/env python
# coding: utf-8

# In[4]:


import argparse, os
import cv2
import numpy as np
import imageio
import time


# In[40]:


def readPicture(picturepath):
    #  open ImageObject
    img = cv2.imread(picturepath, cv2.IMREAD_UNCHANGED)#cv2.IMREAD_UNCHANGED is important that the output is (x,y,ChannelRGB)
    #print(img.shape)
    #alternative
    #img=imageio.imread(picturepath) #liest Bild von picturepath
    return(img)


# In[6]:


def savePic(picture,fileName,extention,outPath):
    outPath = outPath+fileName+'.'+extention # combines the path with the name and extention of the file
    print(outPath)
    try:
        #imageio.imwrite(outPath,picture,format=extention)# old way
        cv2.imwrite(outPath,picture)#saves Pictures 
    except:
        print('Failed while saving picture: '+fileName+' to '+ outPath+' sorry :(') #writes an error
        print('--------------------')


# In[7]:


def YUVtoRGB(img):
    pictureYUV = cv2.cvtColor(img, cv2.COLOR_YUV2RGB, cv2.IMREAD_UNCHANGED) #uses the CV2 method to convert the color space from YU-V to RGB
    return pictureYUV


# In[8]:


def RGBtoYUV(img):
    pictureYUV = cv2.cvtColor(img, cv2.COLOR_RGB2YUV, cv2.IMREAD_UNCHANGED) #uses the CV2 method to convert the color space from RGB to YU-V
    return pictureYUV


# In[9]:


def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min() # searches for the smalest number in the img array and saves it in imin
    imax = img.max() # searches for the biggest number in the img array and saves it in imax

    a = (target_type_max - target_type_min) / (imax - imin) # creates ratio of wanted to actual number value space
    b = target_type_max - a * imax # Creates the maximal possible value in b
    try:
        new_img = (a * img + b).astype(target_type) # recalculates the image with the calculated values and sets the new type
    except:
        print('error while converting the image')
    return new_img


# In[34]:


def hdrorpng(extention,yuvPic):
    if (extention == 'hdr'): # when hdr than normalize in values between 0 and 1
        yuvPic = convert(yuvPic, 0, 1, np.float32) # send to convert in float 32 // Just devide by (2 ** 10) - 1?
    if (extention == 'png'): # when hdr than normalize in values between 0 and 255
        yuvPic = convert(yuvPic, 0, 255, np.uint8) # normalisation to unit8
    return yuvPic
    


# In[18]:


#toDo Add parser with args
###### Imput section
path = input('Path to pictures who should be converted defaut: ./yuvPic/: ') or './yuvPic/'
inputextention = input('What fileextention do the to read pictures have? [default: png]') or 'png'
outputextention = input('Please type outputextention[default: hdr]: ') or 'hdr'
outputpath = input('Where to write the stiched pictures to? [default: ./hdrOut/]: ') or './hdrOut/'
namePic = input('What should be the name of the stiched pictures? [default: pred]') or 'predictedPic'
wantYUV = input('Do you want to keep YUV color space type y? [deflaut: no (RGB_color space)]') or 'no'
aOp = sum(1 for f in os.listdir(path) if f.endswith('.'+inputextention)) #summ all ending with extention


# In[37]:


#Working Version 10022021
start_time = time.time() #start Timer
print('Pictures in the folder need to have the format: [number]-[y]or[u]or[v].png e.g. : 28-y_pred.png,28-u_pred.png,28-v_pred.png')
#TO DO Parser
#desc ='yuv to RGB'
#parser = argparse.ArgumentParser(description=desc)
#parser.add_argument('--yuv', type=str, default='./', help='path to Folder of yuv images')
#print(parser.parse_args())
#what, b = parser.parse_known_args()

#if what.yuv == './' :
 #   print('yes')
start_time = time.time()
i = 0
print(aOp)
while (i <= aOp-1 ): # read y
    if ((str(os.listdir(path)[i]).split('-')[1]).split('_')[0]) == 'y': # only searching for y picitures
        name = os.listdir(path)[i] #finding the Name
        print(name +' should be the Y')
        picpath = path + name #combining Name and path
        picy = readPicture(picpath) #reads a pic y to find the x,y axes should be the same for all pictures
        yuvPic = np.zeros((int(picy.shape[0]),int(picy.shape[1]),3)) # generates the x and y achses and channels of picture
        yuvPic[:,:,1] = picy # packs the Y in pos 1
        num = (str(os.listdir(path)[i]).split('-')[0])#.split('_')[0]
        newPic = path + num + '-u_'+name.split('_')[1]
        picu = readPicture(newPic)#reads a picture with Ending U
        yuvPic[:,:,0] = picu # packs the u in pos 0
        newPic = path + num + '-v_'+name.split('_')[1] #Generates the Name for v
        picv = readPicture(newPic)#reads the new picture with ending V
        yuvPic[:,:,2] = picv # packs the u in pos 2
        #Right for the Testdata ist: 0y2u1v <<<<<<<<<<<<<

        if(wantYUV != 'y'):
            yuvPic = hdrorpng(outputextention,yuvPic) # normalize after conversion
            rgbPic = YUVtoRGB(yuvPic) # to YUV to RGB conversion Matrix needs to have the Format Y[0] U[1] V[2]
            savePic(rgbPic,(str(i)+namePic),outputextention,outputpath)#saves final RGB pic
        if(wantYUV == 'y'):
            yuvPic = hdrorpng(outputextention,yuvPic) # normalize after conversion
            yuvPic = YUVtoRGB(yuvPic)
            savePic(yuvPic,(str(i)+namePic),outputextention,outputpath)#saves final YUV pic
    i = i + 1

print("--- %s seconds ---" % (time.time() - start_time))
print(str((time.time() - start_time)/60))
print('------------------------- Done --------------------')


# In[ ]:





# In[ ]:




