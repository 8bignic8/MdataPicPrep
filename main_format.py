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
    img = cv2.imread(picturepath, cv2.IMREAD_UNCHANGED)# | cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    #old
    #imageio.plugins.freeimage.download()
    #img=imageio.imread(picturepath) #liest Bild von picturepath
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


# In[ ]:





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


def cutPatch(begX,begY,endX,endY,picyx):#cuts out a array of a given array
    try: 
        picyx = picyx[begY:endY,begX:endX] #format y,start:End | x,start:End
    except:
        print('FormatMaking Failed')
    return picyx #returns a small part of the pic file


# In[7]:


def Randtone_map():
        #a random tonemapping is returned
        rand = random.SystemRandom()
        tmNumber = round((rand.randint(0, 30)/10)) # generates a random tonempaiing nuber 
        try:
            if (tmNumber<=0):
                return 'reinhard' #retruns the name of the tonemapper
            if (tmNumber==1):
                return 'mantiuk'
            if (tmNumber==2):
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
    print('All patches will be: '+str(arraysize))
    return arraysize         


# In[9]:


def patchesxy(inputpic,px,py): #calculates how often the array can be devided by px in x and py in y
    arraysize = []
    try:
        y = int(inputpic.shape[0]/py)# calculates the number of patches in the Y-axses cuts the picture i
        x = int(inputpic.shape[1]/px)
        arraysize = (x,y)
    except:
        print('fail calc x and y')
    return arraysize
        


# In[10]:


def resizePic(inputpic,factor): #reszizing the inputpic picture keeping the information but scaling it down
    y = int((inputpic.shape[0])/factor) #multiply the Factor
    x = int((inputpic.shape[1])/factor) #multiply the Factor
    pic = cv2.resize(inputpic,(x,y)) 
    return pic


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
    


# In[21]:


#---- input section
#TO DO add parser
        
start_time = time.time() #start the timeing of the Prgramm
path = ''

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
tokonvPic = int(input('how many Pictures do you want to cut into patches? default 2: ') or '2')
print(str(tokonvPic)+' pictures will be cut into patches')
#scale factor for the low resolution is inputed
factor = int(input('Scale factor for Ldr LR [default:2]: ') or "2")
#asks for the px size of the high resolution pictures
xaxis = int(input('X Patch size HDR HR [default:320px]: ') or "320")
print(xaxis)
yaxis = int(input('Y Patch size HDR HR [default:320px]: ') or "320")
print(yaxis)
#user can choose if the pacht-pictures should be in YU-V or RGB
youWantYUV = input('Do you want to convert to yuv default: no') or 'no'
#user can coose in wich folder the .mat file is stored
savein = input('Should patches be saved in .mat file type: (m) oder should ist be saved as pictures (p) or saved as mat and .hdr/.png type: (mp), [default: m] ') or 'm'      
print(savein)
unit_varSdr = (np.float32)
unit_varHdr = (np.float32)
testing = input('Is the dataset for testing purposes? default: no') or 'no'
if (savein == 'm' or savein == 'mp'):
    #user can choose the name for the .mat file
    matName = input('Input Mat name default: data ') or 'data'
    matPath = input('Input Mat directory path: ./matOut/') or './matOut/'
    if not os.path.exists(matPath):
            os.mkdir(matPath)
    jsi = input('Is it for the JSI-GAN converion from float32 to uint8/16? default: no') or 'no'
    if (jsi != 'no'):
        unit_varSdr = (np.uint8)
        print('SDR .mat file will be uint8')
        unit_varHdr = (np.uint16)
        print('HDR .mat file will be uint16')
if (savein == 'p' or savein == 'mp'): #if user wants to output pates in picters he can choose where
    outPathsdr = input('spezify the output path of sdr pictures [default: ./sdrOut/] ') or './sdrOut/' #set the picture save path if it is choosen
    if not os.path.exists(outPathsdr):
            os.mkdir(outPathsdr)
    outPathhdr = input('spezify the output path of sdr pictures [default: ./hdrOut/] ') or './hdrOut/' #set the picture save path if it is choosen
    if not os.path.exists(outPathhdr):
        os.mkdir(outPathhdr)
    #TO DO if files should all have the same name or original Filename  


# In[22]:


### write pic to .mat and/or .hdr/.png

#Just for general information Data Structure JSI-Gan
###['SDR_data'][79][79][2][39839] dtype=uint8 Strukture .mat Data
###['HDR_data'][79][79][2][39839] dtype=uint16 Strukture .mat Data
    

#---- programm section
allpatches = totalpatchespossible(path,amountOfPictures,extention,xaxis,yaxis,tokonvPic)  #calc all output patches
#print(str(allpatches)+'all Patches')

hdrarray = np.zeros((xaxis,yaxis,3,allpatches))#create empty np array of the size of allpatches
hdrarray = hdrarray.astype(unit_varHdr) #changes the type of np array to uint16
xldr = int(xaxis/factor) #calculates the samler array axes x
yldr = int(yaxis/factor)#calculates the samler array axes y
sdrarray = np.zeros((xldr,yldr,3,allpatches)) # creates the np array for the LR SDR array with new axes
sdrarray = sdrarray.astype(unit_varSdr)#changes the type of np array to uint8
#Arrays are defined in [amountOfallPatchesPossible,x,y,RGB]

print('Start processing...')
tokonvPic= (amountOfPictures-tokonvPic)# the amount of pictures cut into pachtes is calculated
allpatchesSave = allpatches #all pachtes are saved
amountOfPictures = amountOfPictures - 1 # needs to count down because while counts to more than in amonut of Pictures
while (amountOfPictures >= tokonvPic): #filling Array with pachtes from high to low, beginning with the hightes Number
    currentFile = os.listdir(path)[amountOfPictures] #currentFile holds the name of the current position file 
    try:
        if (currentFile.split('.')[1] == str(extention)): #checks if file is ending as wanted
            he = (path+str(currentFile))#gives the path and name with extention of the to process file
            print('processing the picture: '+he) #prints it to the user
            originalPicture = readThePicture(he) #reads the currentpicture and saves it
            
            print(originalPicture.max())
            begX = 1 #startingnumber in wich the cutting starts in X-axes
            endX = xaxis # sets current start pixel position at wich the cutting starts in X
            pxy=patchesxy(originalPicture,xaxis,yaxis) # gives back the length of the current picture (numx,numy) e.g. (3,2)
            px= pxy[0] #saves the max x pos in px
            py= pxy[1] #saves the max y pos in py
            
            while (px >= begX): # cut until you are at the beginning of the picture X position
                begY = 1 #startingnumber in wich the cutting starts in Y-axes
                endY = yaxis # sets current start pixel position at wich the cutting starts in Y
                x = (begX*xaxis)-xaxis #start patch position in x
    
                while (py>=begY): # cut until you are at the beginning of the picture Y position
                    ### reading the picture and cutting section
                    y = (begY*yaxis)-yaxis #start patch position in y
                    patch = cutPatch(x,y,endX,endY,originalPicture) #make the patch and return it to the patch (floart64) array
                    tmo = Randtone_map() # returns a random name for the tonemapping Operator to use
                    
                    patchLR = resizePic(patch,factor) #resize picture from Patch with the factor
                    tmoed = tMO(patchLR,tmo) #tonemap the resized patch with the before chosen Tone Mapping Operator
                    print(tmoed)
                    patch_lrtm = tmoed
                    ####Color YUV Section
                    if (youWantYUV != 'no'): #if change to yuv
                        patch_lrtm = RGBtoYUV(tmoed) # changes the color space of lr sdr array
                        patch = RGBtoYUV(patch) # changes the color space of hr hdr array
                    ###Picture section
                    ### Pictures will be saved as 8bit .png with the picture beeing between 0- 255 uint8
                    ### and 16 bit .hdr with the picture beeing between 0- 2^16 float16
                    print('HDR MAX')
                    if (savein == 'p' or savein == 'mp'): #save as picture if chosen
                        buildFilename = ((currentFile.split('.')[0])+'_'+str(allpatches-1))#builds output name 
                        # TODO Add a Input for the wanted out_format
                        if(testing != 'no'):
                            spaceIndi = 'u','v','y' #orders the Name to the right place
                            savePic((patch_lrtm[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'png',outPathsdr)#saves final singel color channel Picture
                            savePic((patch_lrtm[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'png',outPathsdr)#saves final singel color channel Picture
                            savePic((patch_lrtm[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'png',outPathsdr)#saves final singel color channel Picture
                            savePic((patch[:,:,0]),(str(allpatches-1)+'-'+spaceIndi[0]),'hdr',outPathhdr)#saves final singel color channel Picture
                            savePic((patch[:,:,1]),(str(allpatches-1)+'-'+spaceIndi[1]),'hdr',outPathhdr)#saves final singel color channel Picture
                            savePic((patch[:,:,2]),(str(allpatches-1)+'-'+spaceIndi[2]),'hdr',outPathhdr)#saves final singel color channel Picture
                            ###To DO make 16 bit PNG
                        if(testing == 'no'):
                            savePic(patch,buildFilename,'hdr',outPathhdr)#change 'hdr' here for different HDR-picture save
                            savePic(patch_lrtm,buildFilename,'png',outPathsdr)#chnage 'png' here for different LDR-picture save 
                    #### uint Section
                    print('ABC_1')
                    print(patch_lrtm)
                    #patch_lr = patch_lrtm/((2 ** 8)-1) # normalize between 0,1 in float 32
                    #print('patchMax')
                    #print(patch.max())
                    #patch = patch/((2 ** 16)-1) #convert(patch,0,1) #normalize between 0,1 in float 32
                    if(unit_varHdr == np.uint16):
                        patch_lr = patch_lrtm * ((2 ** 8)-1) 
                        patch = patch * ((2 ** 10)-1) #HDR is changed so it fitts the unit16 OR UInt10?? format and can be compared
                        print('HDR')
                        print(patch.max())
                        print(patch.min())
                        print('LDR')
                        print(patch_lr.max())
                        print(patch_lr.min())
                        patch_lr = patch_lr.astype(unit_varSdr) #changes the data type in according to JSI Gan spec to uint8 for lr sdr
                        patch = patch.astype(unit_varHdr) #changes the data type in according to JSI Gan spec to uint16 for hr hdr
                    
                    ###writing array section 
                    p = (allpatches-1) #calcualte current patch position
                    try:
                        print(patch_lr.shape)
                        sdrarray[:,:,:,p] = patch_lr # try Write the tmoed Patch to sdrarray at current patch position
                    except:
                        print('Error at SDR- Array Writing :..(')
                    try:
                        print(patch.shape)
                        hdrarray[:,:,:,p] = patch # try Write the hr hdr Patch to hdrarray at current patch position
                    except:
                        print('Error at HDR- Array Writing :..(')
                        
                    begY = begY + 1 #Counts up from 1 to all possible cuts of the current picture in Y
                    endY = endY + yaxis #Counts up the position from endY in yaxis steps
                    allpatches = allpatches - 1 #Counts down all patches of all pictures to 0
                    print('Patch === '+str(allpatches)+' ==> Done')
                begX = begX + 1 #Counts up from 1 to all possible cuts of the current picture in X
                endX = endX + xaxis # Counts up the position from endX in xaxis steps
    except:
        print('Error with data maybe not an .hdr file continuing...')  
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

print(str((time.time() - start_time)/60)+' Minutes') #outputs the time in minutes
print('------------------------- Done --------------------')


# In[41]:


#python3 main.py --phase train --scale_factor 2 --train_data_path_LR_SDR ./SDR_data.mat --train_data_path_HR_HDR ./HDR_data.mat --epoch 5 --batch_size 4


# In[93]:


#a = np.count_nonzero(sdrarray)


# In[94]:


#np.count_nonzero(hdrarray)
#hdrarray.any()
#np.all(hdrarray)


# In[21]:


#python3 train.py --batch_size 100 -d ./hdrData -s ./pathToSaceChepoints 


# In[20]:


#python3 main.py --phase test_mat --scale_factor 2 --train_data_path_LR_SDR ./SDR_data.mat --train_data_path_HR_HDR ./HDR_data.mat --test_data_path_LR_SDR /home/nico/programm/MdataPicPrep/matOut/SDR_data.mat --test_data_path_HR_HDR /home/nico/programm/MdataPicPrep/matOut/HDR_data.mat --batch_size 4

