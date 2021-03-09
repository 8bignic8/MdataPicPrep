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
#from IPython.display import Image


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
            tom = cv2.createTonemapReinhard()
        if (name == 'mantiuk'):
            tom = cv2.createTonemapMantiuk()
        if (name == 'drago'):
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
    outPath = outPath+fileName+'.'+extention
    try:
        #old
        #imageio.imwrite(outPath,picture,format=extention)#extention'')#save the Data (path with name and file extention,PictureMatrix,format)
        #new
        cv2.imwrite(outPath,picture)
        print(outPath+'<=== Writing')
    except:
        print('Failed while saving picture: '+fileName+' to '+ outPath+' sorry :(')
        print('--------------------')


# In[6]:


def cutPatch(begX,begY,endX,endY,picxy):#cuts out a array of a given array
    try: 
        picxy = picxy[begX:endX,begY:endY] #format x,start:End | y,start:End 
    except:
        print('FormatMaking Failed')
    return picxy #returns a small part of the pic file


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


def patchesxy(inputpic,px,py): #calculates how often the array can be devided by px in x and py in y
    arraysize = []
    try:
        y = int(inputpic.shape[1]/py)# calculates the number of patches in the Y-axses cuts the picture i
        #print('y'+str(inputpic.shape[1]))
        x = int(inputpic.shape[0]/px)
        #print('x'+str(inputpic.shape[0]))
        arraysize = (x,y)
    except:
        print('fail calc x and y')
    return arraysize
        


# In[10]:


def resizePic(inputpic,factor): #reszizing the inputpic picture keeping the information but scaling it down
    y = int((inputpic.shape[1])/factor) #multiply the Factor in X[0],Y[1] config
    x = int((inputpic.shape[0])/factor) #multiply the Factor
    pic = cv2.resize(inputpic,(x,y))
    #print(pic.shape)
    pic = np.reshape(pic,(pic.shape[1],pic.shape[0],pic.shape[2]))
    #print('Reshaped'+str(pic.shape))
    return pic


# In[ ]:





# In[11]:


def RGBtoYUV(img): #changeing the img picture from RGB- to YUV-Color space
    pictureYUV = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    return pictureYUV


# In[12]:


def YUVtoRGB(img):#changeing the img picture from YUV- to RGB-Color space
    pictureRGB = cv2.cvtColor(img, cv2.COLOR_YUV2RGB)
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


def returnPosFromNumber(xMax,yMax, pos): #should return one coordinat in x and y cunts up from 0 to pos-1
    #allpos = xMax*yMax
    pos = pos-1
    x = 0
    y = pos // xMax #modulo
    x = pos % xMax
    return x+1,y+1


# In[16]:


#---- input section
#TO DO add parser
        
start_time = time.time() #start the timeing of the Prgramm
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

amountOfPictures = sum(1 for f in os.listdir(path) if f.endswith('.'+extention)) #summ all data ending with right extention
print('There are: '+str(amountOfPictures)+' '+extention+' Pictures in the folder')
#User can choose how many pictures should be cut in patches
tokonvPic = int(input('how many Pictures do you want to cut into patches? default 1: ') or '1')
print(str(tokonvPic)+' pictures will be cut into patches')
#scale factor for the low resolution is inputed
factor = int(input('Scale factor for Ldr LR [default:2]: ') or "2")
#asks for the px size of the high resolution pictures
print('The first picture has the shape (y,x, color)'+str(readThePicture(path+str(os.listdir(path)[amountOfPictures-1])).shape))
xaxis = int(input('X Patch size from HDR HR Patch in px [default:420px]: ') or "420")
print(xaxis)
yaxis = int(input('Y Patch size from HDR HR Patch in px [default:420px]: ') or "420")
print(yaxis)
#user can choose if the pacht-pictures should be in YU-V or RGB
youWantYUV = input('Do you want to convert to yuv default: no ') or 'no'
#user can coose in wich folder the .mat file is stored
savein = input('Should patches be saved in .mat file type: (m) oder should ist be saved as pictures (p) or saved as mat and .hdr/.png type: (mp), [default: m] ') or 'm'      
print(savein)
unit_varSdr = (np.float32)
unit_varHdr = (np.float32)
testing = input('Is the dataset for testing purposes or do you want to split the output pictures in cromagan single png pictures? default: no') or 'no'
if (savein == 'p' or savein == 'mp'):
    hrImgOut = input('Should the hdr pictures have the format hdr(yes) or png 16bit(no)? default: no (png 16bit)') or 'no'
if (savein == 'm' or savein == 'mp'):
    #user can choose the name for the .mat file
    matName = input('Input Mat name default: data ') or 'data'
    matPath = input('Input Mat directory path: ./matOut/ ') or './matOut/'
    if not os.path.exists(matPath):
            os.mkdir(matPath)
    jsi = input('Is it for the JSI-GAN converion from float32 to uint8/16? default: no ') or 'no'
    if (jsi != 'no'):
        unit_varSdr = (np.uint8)
        print('SDR .mat file will be uint8')
        unit_varHdr = (np.uint16)
        print('HDR .mat file will be uint16')
if (savein == 'p' or savein == 'mp'): #if user wants to output pates in picters he can choose where
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
patchAmount = input('How many patches do you want to cut out of each Picture? default: 30- ') or '30'


# In[17]:


### write pic to .mat and/or .hdr/.png

#Just for general information Data Structure JSI-Gan
###['SDR_data'][79][79][2][39839] dtype=uint8 Strukture .mat Data
###['HDR_data'][79][79][2][39839] dtype=uint16 Strukture .mat Data
    

#---- programm section

allpatches = int(patchAmount)*int(tokonvPic) # calculates the amount of pictures total
print('That will be ==> '+str(allpatches)+' Patches in total :)')
xldr = int(xaxis/factor) #calculates the samler array axes x
yldr = int(yaxis/factor)#calculates the samler array axes y
#print('XAch'+str(xaxis))
#print('YAch'+str(yaxis))
if (savein == 'm' or savein == 'mp'):
    hdrarray = np.zeros((xaxis,yaxis,3,allpatches))#create empty np array of the size of allpatches
    hdrarray = hdrarray.astype(unit_varHdr) #changes the type of np array to uint16
    sdrarray = np.zeros((xldr,yldr,3,allpatches)) # creates the np array for the LR SDR array with new axes
    sdrarray = sdrarray.astype(unit_varSdr)#changes the type of np array to uint8


#Arrays are defined in [amountOfallPatchesPossible,x,y,RGB]

print('Start processing...')
tokonvPic= (int(amountOfPictures)-int(tokonvPic))# the amount of pictures cut into pachtes is calculated

print(tokonvPic)
print(amountOfPictures)
while (amountOfPictures > tokonvPic):#tokonvPic): #filling Array with pachtes from high to low, beginning with the hightes Number
    currentFile = os.listdir(path)[amountOfPictures-1] #currentFile holds the name of the current position file 
    try:
        if (currentFile.split('.')[1] == str(extention)): #checks if file is ending as wanted
            he = (path+str(currentFile))#gives the path and name with extention of the to process file
            print('processing the picture: '+he) #prints it to the user
            originalPicture = readThePicture(he) #reads the currentpicture and saves it
            originalPicture = originalPicture / ((2 ** 10)-1) #nicht sicher
            print(originalPicture.shape)
            originalPicture = np.reshape(originalPicture,(int(originalPicture.shape[1]),int(originalPicture.shape[0]),int(originalPicture.shape[2]))) #rearanging in XYC
            pxy=patchesxy(originalPicture,xaxis,yaxis) # gives back the length of the current picture (numx,numy) e.g. (3,2)
            px= pxy[0] #saves the max x pos in px
            py= pxy[1] #saves the max y pos in py
            patchCuts = randArray((px*py),int(patchAmount))# returns a array with amount patchAmount and the random positions to cut
            aktPatch = 0
            savePXY = px,py
            while (aktPatch < int(patchAmount)): # cut until you are at the beginning of the picture X position

                randPosXY = returnPosFromNumber((savePXY[0]),(savePXY[1]),int(patchCuts[(aktPatch)])) #returns the x,y coordinate within a given position
                aktPatch = aktPatch + 1
                begy = randPosXY[1]* yaxis #is the new begin Pos in y
                begx = randPosXY[0]* xaxis #is the new begin Pos in x

                px = begx - xaxis #is the new end Pos in x
                py = begy - yaxis #is the new end Pos in Y

                patch = cutPatch(px,py,begx,begy,originalPicture) #make the patch and return it to the patch (floart64) array
                tmo = Randtone_map() # returns a random name for the tonemapping Operator to use     
                patchLR = resizePic(patch,factor) #resize picture from Patch with the factor
                tmoed = tMO(patchLR,tmo) #tonemap the resized patch with the before chosen Tone Mapping Operator
                patch_lrtm = tmoed
                
                    ####Color YUV Section
                if (youWantYUV != 'no'): #if change to yuv
                    patch_lrtm = RGBtoYUV(tmoed) # changes the color space of lr sdr array
                    patch = RGBtoYUV(patch) # changes the color space of hr hdr array
                    
                    ###Picture section
                    ### Pictures will be saved as 8bit .png with the picture beeing between 0- 255 uint8
                    ### and 16 bit .hdr with the picture beeing between 0- 2^16 float16
                if (savein == 'p' or savein == 'mp'): #save as picture if chosen
                        #buildFilename = ((currentFile.split('.')[0])+'_'+str(allpatches-1))#builds output name 
                    buildFilename = str(allpatches-1).zfill(6)# gives the filename only an number filled up with 6 zeros (mybe better if zeros from max allpatches)
                        
                        # TODO Add a Input for the wanted out_format
                    patch_lrtmp = patch_lrtm * ((2 ** 8)-1)
                    if(testing != 'no'):
                        spaceIndi = 'y','u','v' #orders the Name to the right place
                        savePic((patch_lrtmp[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'png',outPathsdr)#saves final singel color channel Picture y
                        savePic((patch_lrtmp[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'png',outPathsdr)#saves final singel color channel Picture u
                        savePic((patch_lrtmp[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'png',outPathsdr)#saves final singel color channel Picture v
                            
                            ####Saveing the 16Bit HDR picturespatches
                        if(hrImgOut !='no'):
                            patchbic = patch * ((2 ** 10)-1)
                            savePic((patchbic[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'hdr',outPathhdr)#saves final singel color channel Picture
                            savePic((patchbic[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'hdr',outPathhdr)#saves final singel color channel Picture
                            savePic((patchbic[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'hdr',outPathhdr)#saves final singel color channel Picture
                            
                            
                            #Saveing the 16Bit PNG output picturepachtes
                        if(hrImgOut == 'no'):
                            patchbic = patch * 2*((2 ** 10)-1) #2* delete?
                            patchbic = patchbic.astype(np.uint16)
                            print('(HDR)-PNG is 16 bit')
                            savePic((patchbic[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'png',outPathhdr)#saves final singel color channel Picture
                            savePic((patchbic[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'png',outPathhdr)#saves final singel color channel Picture
                            savePic((patchbic[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'png',outPathhdr)#saves final singel color channel Picture
                            
                            ###To DO make 16 bit PNG
                    if(testing == 'no'):
                        if(hrImgOut == 'no'):
                            patchpic = patch * ((2 ** 16)-1)
                            patchpic = patchpic.astype(np.uint16)
                            savePic(patchpic,buildFilename,'png',outPathhdr)#change 'hdr' here for different HDR-picture save
                        if(hrImgOut != 'no'):
                            savePic(patch,buildFilename,'hdr',outPathhdr)#change 'hdr' here for different HDR-picture save    
                        savePic(patch_lrtmp,buildFilename,'png',outPathsdr)#chnage 'png' here for different LDR-picture save 

                if(unit_varHdr == np.uint16):
                    patch_lrtm = patch_lrtm * ((2 ** 8)-1) 
                    patch = (patch * ((2 ** 10)-1)) * ((2 ** 10)-1) #HDR is changed so it fitts the unit16 format and can be compared
                    patch_lr = patch_lrtm.astype(unit_varSdr) #changes the data type in according to JSI Gan spec to uint8 for lr sdr
                    patch = patch.astype(unit_varHdr) #changes the data type in according to JSI Gan spec to uint16 for hr hdr
                    
                    
                    ###writing complete array section 
                p = (allpatches-1) #calcualte current patch position
                if (savein == 'm' or savein == 'mp'):
                        #if(unit_varHdr == np.uint8):
                        #patch_lrtm = patch_lrtm * ((2 ** 8)-1)
                    try:
                            #print(patch_lrtm.shape)
                        print(patch_lrtm.max())
                        #patch_lrtm = patch_lrtm / ((2 ** 8)-1)
                        print(patch_lrtm.max())
                        patch_lrtm = np.clip(patch_lrtm, 0, 1)
                        #print(patch_lrtm.max())
                        sdrarray[:,:,:,p] = patch_lrtm # try Write the tmoed Patch to sdrarray at current patch position
                    except:
                        print('Error at SDR- Array Writing :..(')
                    try:
                        print(patch.max())
                        #patch = patch / ((2 ** 10)-1)
                        patch = np.clip(patch, 0, 1)
                        print('patchShape-'+str(patch.shape))
                        hdrarray[:,:,:,p] = patch # try Write the hr hdr Patch to hdrarray at current patch position
                    except:
                        print('Error at HDR- Array Writing :..(')
                        
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
        print(str(patch_lrtm.shape)+' sdrPatchShape')
        
    amountOfPictures = amountOfPictures - 1 #counts down current picture pos
    #print(str(amountOfPictures)+'AmountOf Pic')
    
    
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


# In[18]:


#python3 main.py --phase train --scale_factor 2 --train_data_path_LR_SDR ./SDR_data.mat --train_data_path_HR_HDR ./HDR_data.mat --epoch 5 --batch_size 4


# In[18]:


### gives the amount of nuberst larger than 0 in percent
#np.count_nonzero(ab)
#(np.count_nonzero(sdrarray)/sdrarray.size)*100
# np.clip(test_pred, 0, 1) clippes to 0,1
#print(sdrarray)
#print(hdrarray)

#train
 #   python3 main.py --phase train --scale_factor 2 --train_data_path_LR_SDR /mnt/Data/nige8437/MdataPicPrep/matOut/SDR_data.mat --train_data_path_HR_HDR /mnt/Data/nige8437/MdataPicPrep/matOut/HDR_data.mat --batch_size 10 --test_img_dir /mnt/Data/nige8437/jsigan/ganOutputdata/
 #test
 
 
 
 
#python3 main.py --exp_num 3 --phase test_mat --scale_factor 2 --train_data_path_LR_SDR /mnt/Data/nige8437/MdataPicPrep/matOut/SDR_myDatue.mat --train_data_path_HR_HDR /mnt/Data/nige8437/MdataPicPrep/matOut/HDR_myDatue.mat --test_data_path_LR_SDR /mnt/Data/nige8437/MdataPicPrep/matOut/SDR_data.mat --test_data_path_HR_HDR /mnt/Data/nige8437/MdataPicPrep/matOut/HDR_data.mat --test_img_dir /mnt/Data/nige8437/jsigan/ganOutputdata/ --batch_size 1

python3 main.py --phase test_mat --scale_factor 2 --train_data_path_LR_SDR
/mnt/Data/nige8437/MdataPicPrep/matOut/SDR_data.mat --train_data_path_HR_HDR
/mnt/Data/nige8437/MdataPicPrep/matOut/HDR_data.mat --test_data_path_LR_SDR
/mnt/Data/nige8437/jsigan/test_input/testset_SDR_x2.mat --test_data_path_HR_HDR /mnt/Data/nige8437/jsigan/test_input/testset_HDR.mat --test_img_dir /mnt/Data/nige8437/jsigan/ganOutputdata/ --batch_size 10




python3 main.py --exp_num 1  --phase test_mat --scale_factor 2 --train_data_path_LR_SDR /home/nico/mnt/cutRawData/matOut/SDR_data.mat --train_data_path_HR_HDR /home/nico/mnt/cutRawData/matOut/HDR_data.mat --test_data_path_LR_SDR /home/nico/mnt/cutRawData/jsiGan_test/testset_SDR_x2.mat --test_data_path_HR_HDR /home/nico/mnt/cutRawData/jsiGan_test/testset_HDR.mat --test_img_dir /home/nico/mnt/cutRawData/jsiGanOutput/ --batch_size 4
    
    
# In[19]:


#np.count_nonzero(ab)
#hdrarray.max()
#(np.count_nonzero(hdrarray)/hdrarray.size)*100


# In[21]:


#python3 train.py --batch_size 100 -d ./hdrData -s ./pathToSaceChepoints 


# In[22]:


#python3 main.py --phase test_mat --scale_factor 2 --train_data_path_LR_SDR ./SDR_data.mat --train_data_path_HR_HDR ./HDR_data.mat --test_data_path_LR_SDR /home/nico/programm/MdataPicPrep/matOut/SDR_data.mat --test_data_path_HR_HDR /home/nico/programm/MdataPicPrep/matOut/HDR_data.mat --batch_size 4

