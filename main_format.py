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
import random
import time
import argparse
#from IPython import display
#from IPython.display import Image, display


# In[2]:


#Read Picture and return it

def readThePicture(picturepath):
    #  open ImageObject
    try:
        img = cv2.imread(picturepath, cv2.IMREAD_UNCHANGED)# | cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        #old
        #imageio.plugins.freeimage.download()
        #img=imageio.imread(picturepath) #liest Bild von picturepath
    except:
        print('There was an error while reading the picture')
        img = 0
    return(img) #returns picture


# In[3]:


def tMO(file,name): #tonemapping the file
    try:
        if (name == 'reinhard'):
            print('Reinhard')
            tom = cv2.createTonemapReinhard()
        if (name == 'mantiuk'):
            print('Mantiuk')
            tom = cv2.createTonemapMantiuk()
        if (name == 'drago'):
            print('drago')
            tom = cv2.createTonemapDrago()
       # if (name == 'linear'):
        #    tom = cv2.createTonemap()
    except: 
        print('ToneMapping Error')
    ldr = tom.process(file)
    return ldr


# In[4]:


def convert(img, target_type_min, target_type_max): # converts the input array to a target type with the bounderys given
    imin = img.min()
    imax = img.max()
    #print(imin)
    a = (target_type_max - target_type_min) / (imax - imin) # generates a factor a to multiply with the img
    b = target_type_max - a * imax
    new_img = (a * img + b)
    return new_img


# In[5]:


def savePic(picture,fileName,extention,outPath): #saves the given array as a pictures to the given output path
    #print('here:)')
    outPath = outPath+fileName+'.'+extention
    #print(outPath)
    try:
        #old
        #imageio.imwrite(outPath,picture,format=extention)#extention'')#save the Data (path with name and file extention,PictureMatrix,format)
        #new
        print(picture.shape)
        print('writePicture')
        cv2.imwrite(outPath,picture)
        print(outPath+'<=== Writing')
    except:
        print('Failed while saving picture: '+fileName+' to '+ outPath+' sorry :(')
        print('--------------------')


# In[6]:


def cutPatchxy(begX,endX,begY,endY,picyx):#cuts out a array of a given array
    try:
        #print('CUTTTING')
        #print(picyx.shape)
        #print(begY-endY,begX-endX)
        picyx = picyx[endY:begY,endX:begX] #format x,start:End | y,start:End 
        #print(picyx.shape)
    except:
        print('FormatMaking Failed')
    return picyx #returns a small part of the pic file


# In[7]:


def Randtone_map():
        #a random tonemapping is returned
        rand = random.SystemRandom()
        tmNumber = round((rand.randint(0, 20)/10)) # generates a random tonempaiing nuber 
        try:
            if (tmNumber<=0):
                return 'reinhard' #retruns the name of the tonemapper
            if (tmNumber==1):
                return 'mantiuk'
            if (tmNumber>=2):
                return 'drago'
           # if (tmNumber>=3):
            #    return 'linear'
        except:
            print('there was an tmo Error')
#ToDo Output in CSV to later analize


# In[8]:


def totalpatchespossible(path,amountOfPictures,extention,px,py,tokonvPic): #calculates the amount of total possible patches of the path you picked 
    arraysize = 0 #zero the output
    amountOfPictures = amountOfPictures - 1
    tokonvPic= (amountOfPictures-(tokonvPic))+1 #generates the stop argument 
    while (amountOfPictures) >= tokonvPic:
        try:
            helping = os.listdir(path)[amountOfPictures].split('.')[1] #reading the File extention
            if ( helping == extention): #only counts files with the same extention
                he = (path+str(os.listdir(path)[amountOfPictures])) #reading path to picture
                print(he) #prints the name of the picture what is currently been read
                readPic = readThePicture(he)
                arraysize = arraysize + (int(readPic.shape[1]/px)*int(readPic.shape[0]/py))# calculate the whole size an cut away the rest even when 0.9
        except:
            print('fail count all patches')
        amountOfPictures = amountOfPictures - 1
    print('There will be >> '+str(arraysize)+' << total patches')
    return arraysize         


# In[9]:


def patchesyx(inputpic,py,px): #calculates how often the array can be devided by px in x and py in y
    arraysize = []
    try:
        y = int(inputpic.shape[0]/py)# calculates the number of patches in the Y-axses cuts the picture i
        #print('y'+str(inputpic.shape[1]))
        x = int(inputpic.shape[1]/px)
        #print('x'+str(inputpic.shape[0]))
        arraysize = (y,x)
    except:
        print('fail calc x and y')
    return arraysize
        


# In[10]:


def resizePic(inputpic,factor): #reszizing the inputpic picture keeping the information but scaling it down    
    y = int((inputpic.shape[0])/factor) #multiply the Factor in X[0],Y[1] config
    x = int((inputpic.shape[1])/factor) #multiply the Factor
    dim = (x, y)
    #print(inputpic.shape)
    #inputpic = np.reshape(inputpic,(inputpic.shape[1],inputpic.shape[0],inputpic.shape[2])) #rotate 180degree
    pic = cv2.resize(inputpic,dim, interpolation = cv2.INTER_AREA)
    
    #print('Reshaped'+str(pic.shape))
    return pic


# In[ ]:





# In[11]:


def RGBtoYUV(img): #changeing the img picture from RGB- to YUV-Color space
    pictureYUV = cv2.cvtColor((img), cv2.COLOR_BGR2YUV, cv2.IMREAD_UNCHANGED)
    #pictureRGB = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
    
    #different Method
    #im_rgb = img.astype(np.float32)
    #im_ycrcb = cv2.cvtColor(im_rgb, cv2.COLOR_RGBE2YCR_CB)
    #im_ycbcr = im_ycrcb[:,:,(0,2,1)].astype(np.float32)
    #im_ycbcr[:,:,0] = (im_ycbcr[:,:,0]*(235-16)+16)/255.0 #to [16/255, 235/255]
    #im_ycbcr[:,:,1:] = (im_ycbcr[:,:,1:]*(240-16)+16)/255.0 #to [16/255, 240/255]

    return pictureYUV


# In[12]:


def YUVtoRGB(img):#changeing the img picture from YUV- to RGB-Color space
    #pictureRGB = cv2.cvtColor(img, cv2.COLOR_YUV2RGB, cv2.IMREAD_UNCHANGED)
    #https://stackoverflow.com/questions/26480125/how-to-get-the-same-output-of-rgb2ycbcr-matlab-function-in-python-opencv
    #https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html
    pictureRGB = cv2.cvtColor((img), cv2.COLOR_YUV2BGR, cv2.IMREAD_UNCHANGED)
    
    return pictureRGB


# In[13]:


#TO Finish
def inputargs():#todo finish
    parser = argparse.ArgumentParser()
    parser.add_argument('--foo', help='foo help')
    args = parser.parse_args()
    


# In[14]:


# this function should return an random array with
def randArray(allPatches, patchPerPic): 
    patchRandArray = np.zeros((patchPerPic)) #generates the array
    rand = random.SystemRandom() #starts the rand generator
    while(patchPerPic > 0):
        patchnNum = round(rand.randint(0, allPatches)) #
        if (not(patchnNum in patchRandArray)): #if number is not in array already 
            patchRandArray[patchPerPic-1] = patchnNum #write it in
            patchPerPic = patchPerPic -1
    return patchRandArray


# In[15]:


def returnPosFromNumberXY(xMax,yMax, pos): #should return one coordinat in x and y cunts up from 0 to pos-1
    #allpos = xMax*yMax
    pos = pos-1
    x = 0
    y = 0
    #print(x,y)
    y = pos // yMax #modulo
    #print(x,y)
    x = pos % yMax
    #print(x,y)
    return x,y


# In[16]:


#piccc = readThePicture('/home/nico/programm/MdataPicPrep/sdrOut/000000.png')
#piccc = RGBtoYUV(piccc)
#savePic(piccc,'fileName_asdsad2222as','png',"/home/nico/programm/MdataPicPrep/sdrOut/")


# In[ ]:





# In[28]:


#---- input section
#TO DO add parser
        

path = ''
print('This skript uses a folder and converts the pictures in smaler random Patches in YUV or RGB color space, Use same size file to avoid errors')
#data extention of the input data
extention = input('What fileextention is supposed to be put into patches(e.g. hdr, png) [default: hdr: ]') or 'hdr'
print(extention)
#Where are the rawData at?
path = input('Where is the Path to the pictures (should be .hdr) [default: ./hdrInput/]') or './hdrInput/'
if not os.path.exists(path):
        os.mkdir(path)
print(path)
inhalte = (os.listdir(path)) #list of all files in path
amountOfPictures = 0

keepFileName = input('Do you want to keep the original filename? default: no ') or 'no'

amountOfPictures = sum(1 for f in os.listdir(path) if f.endswith('.'+extention)) #summ all data ending with right extention
print('There are: '+str(amountOfPictures)+' '+extention+' Pictures in the folder')
#User can choose how many pictures should be cut in patches
tokonvPic = int(input('how many Pictures do you want to cut into patches? default 1: ') or '1')
print(str(tokonvPic)+' pictures will be cut into patches')
#scale factor for the low resolution is inputed
factor = int(input('Scale factor for Ldr LR [default:2]: ') or "2")
#asks for the px size of the high resolution pictures
print('The first picture has the shape (y,x, color)'+str(readThePicture(path+str(os.listdir(path)[amountOfPictures-1])).shape))
yaxis = int(input('Y Patch size from HDR HR Patch in py [default:420px]: ') or "600")
print(yaxis)
xaxis = int(input('X Patch size from HDR HR Patch in px [default:420px]: ') or "420")
print(xaxis)
#user can choose if the pacht-pictures should be in YU-V or RGB
youWantYUV = input('Do you want to convert to yuv default: no ') or 'no'
#user can coose in wich folder the .mat file is stored
savein = input('Should patches be saved in .mat file type: (m) oder should ist be saved as pictures (p) or saved as mat and .hdr/.png type: (mp), [default: p] ') or 'p'      
print(savein)
unit_varSdr = (np.float32)
unit_varHdr = (np.float32)
testing = input('Is the dataset for testing purposes or do you want to split the output pictures in cromagan single png pictures? default: no') or 'no'
if (savein == 'p' or savein == 'mp'):
    hrImgOut = input('Should the hdr pictures have the format hdr(yes) or png 16bit(no)? default: no (png 16bit)') or 'no'
if (savein == 'm' or savein == 'mp'):
    #user can choose the name for the .mat file
    matName = input('Output Mat name default: data ') or 'data'
    matPath = input('Output Mat directory path: ./matOut/ ') or './matOut/'
    if not os.path.exists(matPath):
            os.mkdir(matPath)
jsi = input('Is it for the JSI-GAN converion from float32 to uint8/16? default: no ') or 'no'

if (jsi != 'no'):
    unit_varSdr = (np.uint8)
    print('SDR .mat file will be uint8')
    unit_varHdr = (np.uint16)
    print('HDR .mat file will be uint16')
    
if (savein == 'p' or savein == 'mp' or savein == 'm'): #if user wants to output pates in picters he can choose where
    outPathsdr = input('spezify the output path of sdr pictures [default: ./sdrOut/ ] ') or './sdrOut/' #set the picture save path if it is choosen
    if not os.path.exists(outPathsdr):
            os.mkdir(outPathsdr)
    outPathhdr = input('spezify the output path of sdr pictures [default: ./hdrOut/ ] ') or './hdrOut/' #set the picture save path if it is choosen
    if not os.path.exists(outPathhdr):
        os.mkdir(outPathhdr)

        #TO DO if files should all have the same name or original Filename
inhalte
if ((input('do you want to know all patches possible? default: no') or 'no')!='no'):
    allpatches = totalpatchespossible(path,amountOfPictures,extention,xaxis,yaxis,tokonvPic)  #calc all output patches
patchAmount = input('How many patches do you want to cut out of each Picture? default: 3- ') or '3'


# In[29]:


start_time = time.time() #start the timeing of the Prgramm
### write pic to .mat and/or .hdr/.png

#Just for general information Data Structure JSI-Gan
###['SDR_data'],[79Y][79X][2C],[39839Num] dtype=uint8 Strukture .mat Data
###
###['HDR_data'][159][159][2][39839] dtype=uint16 Strukture .mat Data
    

#---- programm section

allpatches = int(patchAmount)*int(tokonvPic) # calculates the amount of pictures total
print('That will be ==> '+str(allpatches)+' Patches in total :)')
xldr = int(xaxis/factor) #calculates the samler array axes x
yldr = int(yaxis/factor)#calculates the samler array axes y
#print('XAch'+str(xaxis))
#print('YAch'+str(yaxis))
if (savein == 'm' or savein == 'mp'):
    hdrarray = np.zeros((yaxis,xaxis,3,allpatches))#create empty np array of the size of allpatches
    hdrarray = hdrarray.astype(unit_varHdr) #changes the type of np array to uint16
    sdrarray = np.zeros((yldr,xldr,3,allpatches)) # creates the np array for the LR SDR array with new axes
    sdrarray = sdrarray.astype(unit_varSdr)#changes the type of np array to uint8


#Arrays are defined in [amountOfallPatchesPossible,x,y,RGB]

print('Start processing...')
tokonvPic= (int(amountOfPictures)-int(tokonvPic))# the amount of pictures cut into pachtes is calculated

#print(tokonvPic)
#print(amountOfPictures)
while (amountOfPictures > tokonvPic):#tokonvPic): #filling Array with pachtes from high to low, beginning with the hightes Number
    currentFile = os.listdir(path)[amountOfPictures-1] #currentFile holds the name of the current position file 
    try:
        if (currentFile.split('.')[1] == str(extention)): #checks if file is ending as wanted
            he = (path+str(currentFile))#gives the path and name with extention of the to process file
            print('processing the picture: '+he) #prints it to the user
            originalPicture = readThePicture(he) #reads the currentpicture and saves it y,x
            #print(originalPicture.shape)
            #originalPicture = np.reshape(originalPicture,(int(originalPicture.shape[1]),int(originalPicture.shape[0]),int(originalPicture.shape[2]))) #rearanging in XYC
            pyx=patchesyx(originalPicture,yaxis,xaxis) # gives back the length of the current picture (numx,numy) e.g. (3,2)
            #print('YX'+str(pyx))
            px= pyx[1] #saves the max x pos in px
            py= pyx[0] #saves the max y pos in py
            patchCuts = randArray((px*py),int(patchAmount))# returns a array with amount patchAmount and the random positions to cut
            #print(patchCuts)
            aktPatch = 0
            savePXY = px,py
            while (aktPatch < int(patchAmount)): # cut until you are at the beginning of the picture X position

                randPosYX = returnPosFromNumberXY((savePXY[0]),(savePXY[1]),int(patchCuts[(aktPatch)])) #returns the x,y coordinate within a given position
                #print('randPosYX')
                #print(randPosYX)
                aktPatch = aktPatch + 1
                begy = randPosYX[0]* yaxis #is the new begin Pos in y
                begx = randPosYX[1]* xaxis #is the new begin Pos in x
                #print('Xaxis')
                #print(xaxis)
                px = begx + xaxis #is the new end Pos in x
                py = begy + yaxis #is the new end Pos in Y
                #print('Position:')
                #print(px,py,begx,begy)
                
                patch = cutPatchxy(px,begx,py,begy,originalPicture) #begX,endX,begY,endY,picyxmake the patch and return it to the patch (floart64) array
                print(patch.shape)
                ###choose your option
                #HDR original with float32
                hdr = patch
                #HDR original in YUV
                hdr_yuv = RGBtoYUV(hdr) 
                #HDR in uint16 with 10bit
                hdr_png = np.clip((hdr*((2**10)-1)), 0, ((2**10)-1)).astype(np.uint16)
                #HDR in uint16 and yuv
                hdr_png_yuv = np.clip((hdr_yuv*((2**10)-1)), 0, ((2**10)-1)).astype(np.uint16) 
                
                ##SDR area
                tmo = Randtone_map()
                sdr_32 = tMO(hdr,tmo) # as float 32
                sdr_32_fac = resizePic(sdr_32,factor)
                #SDR 
                ldr_8 = np.clip((sdr_32_fac*((2**8)-1)), 0, ((2**8)-1)).astype(np.uint8)
                #SDR in YUV
                ldr_8_yuv = (RGBtoYUV(((ldr_8).astype(np.uint8))).astype(np.uint8))
                
                    ####Color YUV Section
                if (savein == 'p' or savein == 'mp'): #save as picture if chosen
                    
                    if(keepFileName == 'yes' ):
                        buildFilename = ((currentFile.split('.')[0])+'_'+str(allpatches-1))# dont delete builds output name 
                    buildFilename = str(allpatches-1).zfill(6)# gives the filename only an number filled up with 6 zeros (mybe better if zeros from max allpatches)
                    
                    if(youWantYUV != 'no'):    
                        # TODO Add a Input for the wanted out_format
                        if((testing != 'no') and (jsi != 'no')):
                            spaceIndi = 'y','u','v' #orders the Name to the right place
                            savePic((ldr_8_yuv[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'png',outPathsdr)#saves final singel color channel Picture y
                            savePic((ldr_8_yuv[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'png',outPathsdr)#saves final singel color channel Picture u
                            savePic((ldr_8_yuv[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'png',outPathsdr)#saves final singel color channel Picture v
                            savePic(ldr_8,buildFilename,'png',outPathsdr) #check Picture
                                ####Saveing the 16Bit HDR picturespatches
                            if(hrImgOut !='no'):
                                savePic((hdr_yuv[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'hdr',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr_yuv[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'hdr',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr_yuv[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'hdr',outPathhdr)#saves final singel color channel Picture
                                savePic(hdr_yuv,buildFilename,'hdr',outPathhdr) #check Picture

                                #Saveing the 16Bit PNG output picturepachtes
                            if(hrImgOut == 'no'):
                                savePic((hdr_png_yuv[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'png',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr_png_yuv[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'png',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr_png_yuv[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'png',outPathhdr)#saves final singel color channel Picture
                                savePic(hdr_png,buildFilename,'png',outPathhdr) #check Picture
                                
                        if(testing == 'no'):
                            if(hrImgOut == 'no'):
                                savePic(hdr_png_yuv,buildFilename,'png',outPathhdr)#change 'hdr' here for different HDR-picture save
                            if(hrImgOut != 'no'):
                                savePic(hdr_yuv,buildFilename,'hdr',outPathhdr)#change 'hdr' here for different HDR-picture save    
                            savePic(ldr_8_yuv,buildFilename,'png',outPathsdr)#chnage 'png' here for different LDR-picture save 

                    
                    #########Normal Section
                    if(youWantYUV == 'no'):
                        print('yuV_no')
                        # TODO Add a Input for the wanted out_format
                        if(testing != 'no'):
                            spaceIndi = 'y','u','v' #orders the Name to the right place
                            savePic((ldr_8[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'png',outPathsdr)#saves final singel color channel Picture y
                            savePic((ldr_8[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'png',outPathsdr)#saves final singel color channel Picture u
                            savePic((ldr_8[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'png',outPathsdr)#saves final singel color channel Picture v
                            savePic(ldr_8,buildFilename,'png',outPathsdr) #check Picture
                                ####Saveing the 16Bit HDR picturespatches
                            if(hrImgOut !='no'):
                                savePic((hdr[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'hdr',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'hdr',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'hdr',outPathhdr)#saves final singel color channel Picture
                                savePic(hdr,buildFilename,'hdr',outPathhdr) #check Picture

                                #Saveing the 16Bit PNG output picturepachtes
                            if(hrImgOut == 'no'):
                                print('(HDR)-PNG is 16 bit')
                                savePic((hdr_png[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'png',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr_png[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'png',outPathhdr)#saves final singel color channel Picture
                                savePic((hdr_png[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'png',outPathhdr)#saves final singel color channel Picture
                                savePic(hdr_png,buildFilename,'png',outPathhdr) #check Pic
                        if(testing == 'no'):
                            if(hrImgOut == 'no'):
                                savePic(hdr_png,buildFilename,'png',outPathhdr)#change 'hdr' here for different HDR-picture save
                            if(hrImgOut != 'no'):
                                savePic(hdr,buildFilename,'hdr',outPathhdr)#change 'hdr' here for different HDR-picture save    
                            savePic(ldr_8,buildFilename,'png',outPathsdr)#chnage 'png' here for different LDR-picture save 
                    
                    ###writing SDR array section 
                p = (allpatches-1) #calcualte current patch position
                if (savein == 'm' or savein == 'mp'):
                    try:
                        if((youWantYUV == 'no') and (jsi == 'no')):
                            print('RGB_noJSI')
                            sdrarray[:,:,:,p] = ldr_8 # clipped the tmoed Picture to 0,1
                            hdrarray[:,:,:,p] = hdr # try Write the Patch to hdrarray at current patch position
                        if((youWantYUV != 'no') and (jsi == 'no')):
                            print('YUV_noJSI')
                            sdrarray[:,:,:,p] = ldr_8_yuv # clipped the tmoed Picture to 0,1
                            hdrarray[:,:,:,p] = hdr_yuv # try Write the Patch to hdrarray at current patch position
                        if((youWantYUV == 'no') and (jsi != 'no')):
                            print('RGB_JSI')
                            sdrarray[:,:,:,p] = ldr_8 # try Write the tmoed Patch to sdrarray at current patch position
                            hdrarray[:,:,:,p] = hdr_png # try Write the Patch to hdrarray at current patch position
                        if((youWantYUV != 'no') and (jsi != 'no')):
                            print('YUV_JSI')
                            sdrarray[:,:,:,p] = ldr_8_yuv # try Write the tmoed Patch to sdrarray at current patch position
                            hdrarray[:,:,:,p] = hdr_png_yuv # try Write the Patch to hdrarray at current patch position     
                    except:
                        print('Error at Array Writing :..(')
                        print(str(originalPicture.shape)+'OrgPicShape')
                        print('BeginHereX '+str(begx)+' to '+str(px))
                        print('beginHereY '+str(begy)+' to '+str(py))
                        print(str(patchCuts.shape)+' PatchCutsAmaount')
                        print(str(aktPatch)+' PatchPos')
                        print(str(patchCuts[(aktPatch)])+' PatchCuts_pos')
                        print(str(patch.shape)+' hdrPatchShape')
                        print(str(png_lr_tmo.shape)+' sdrPatchShape')   
                allpatches = allpatches - 1 #Counts down all patches of all pictures to 0
                print('Patch === '+str(allpatches)+' ==> Done')
                
    except:
        print('Error with data maybe not an .hdr file continuing...')
        print(str(originalPicture.shape)+'OrgPicShape')
        print('BeginHereX '+str(begx)+' to '+str(px))
        print('beginHereY '+str(begy)+' to '+str(py))
        print(str(patchCuts.shape)+' PatchCutsAmaount')
        print(str(aktPatch)+' PatchPos')
        print(str(patchCuts[(aktPatch)])+' PatchCuts_pos')
        print(str(patch.shape)+' hdrPatchShape')
        print(str(png_lr_tmo.shape)+' sdrPatchShape')   
    print(str((time.time() - start_time)/60)+' Minutes to patch nr: '+str(allpatches)) #outputs the time in minutes    
    amountOfPictures = amountOfPictures - 1 #counts down current picture pos
    
if (savein == 'mp' or savein == 'm' ): #only makes a Matlap File if wanted
    try:
        matLabel = 'HDR_data'
        if(testing != 'no'):
            matLabel = 'HDR_YUV'
            print('testdata')
        # Write TO HDR.Mat File
        h5.get_config().default_file_mode = 'a' #write enable
        matfilehdrdataHDR = {} # make a dictionary to store the MAT data in
        print('HDR Matlab file will have the format')
        print(hdrarray.shape)
        matfilehdrdataHDR[u''+matLabel] = hdrarray #save hdr array in that dictonary
        print('Writing HDR_'+matName+'.mat File to: '+ matPath)
        hdf5storage.write(matfilehdrdataHDR, '.', matPath+'HDR_'+matName+'.mat', matlab_compatible=True) #output the .mat data file
        print('Saved the HDR .mat file')

        #####Writing SDR .mat 
        #Switches the first with the last array Field 
        matfilesdrdatasdr = {} # make a dictionary to store the MAT data in
        matLabel = 'SDR_data'
        if(testing != 'no'):
            matLabel = 'SDR_YUV'
            print('testdata')
        print('SDR Matlab file will have the format')
        print(sdrarray.shape)
        matfilesdrdatasdr[u''+matLabel] = sdrarray #save sdr array in that dictonary
        print('Writing SDR_'+matName+'.mat File to: '+ matPath)
        hdf5storage.write(matfilesdrdatasdr, '.', matPath+'SDR_'+matName+'.mat', matlab_compatible=True) #output the .mat data file
        print('Saved the SDR .mat file')
    except:
        print('error at writing matlab file sorry :(')
        
    sdrpro = (np.count_nonzero(sdrarray)/sdrarray.size)*100        
    print(str(sdrpro)+'% of SDRarray numbers are bigger than 0')

    sdrpro = (np.count_nonzero(hdrarray)/hdrarray.size)*100        
    print(str(sdrpro)+'% of HDRarray numbers are bigger than 0')

print(str((time.time() - start_time)/60)+' Minutes') #outputs the time in minutes
print('------------------------- Done --------------------')


# In[ ]:





# In[30]:


ldr_8


# In[26]:


ab = readThePicture('/Users/littledragon/Documents/BA 13022020/programme/MdataPicPrep/sdrOut/000003.png')

ldr_8_b = (RGBtoYUV(((ldr_8).astype(np.uint8))).astype(np.uint8))

#hdr_png_yuv_b = (ldr_8_b).astype(np.uint8)#*127
savePic(ldr_8_b,'fileName_letMeTink','png','./sdrOut/')

ab  = (YUVtoRGB(((ldr_8_b).astype(np.uint8))).astype(np.uint8))
#ab = YUVtoRGB(ab)
savePic((ab),'fileName_letMeTink_rgb','png','./sdrOut/')

ab = (ab/255).astype(np.float32)
savePic((ab),'fileName_letMeTink_rgb_hdr','hdr','./sdrOut/')

#hdr_png_yuv_b.max()


# In[27]:


#hdr_png = hdr*((2**10)-1)
hdr_png_yuv_c = ((hdr)*((2**16)-1)).astype(np.uint16)
hdr_png_yuv_c = RGBtoYUV(hdr_png_yuv_c)

hdr_png_yuv_b = (hdr_png_yuv_c*((2**1)-1)).astype(np.uint16)#*127
savePic(hdr_png_yuv_c,'fileName_letMeTink','png','./sdrOut/')

ab  = (YUVtoRGB(hdr_png_yuv_c*((2**1)-1)).astype(np.uint16))
#ab = YUVtoRGB(ab)
savePic((ab),'fileName_letMeTink_rgb','png','./sdrOut/')

ab = (ab/((2**16)-1)).astype(np.float32)
savePic((ab),'fileName_letMeTink_rgb_hdr','hdr','./sdrOut/')
HDR_test = YUVtoRGB((hdr_png_yuv/((2**10)-1)).astype(np.float32))
savePic(HDR_test,'fileName_letMeTink_rgb_hdr_org','hdr','./sdrOut/')
hdr_png_yuv_c.max()


# In[62]:


ldr_8_b.max()


# In[108]:


hdr_png_yuv_c


# In[ ]:




