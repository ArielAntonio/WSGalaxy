from skimage.util import crop
from matplotlib import patches,  lines
import numpy as np

from astropy.io import ascii
from astropy.table import Table, Column, join, vstack, hstack
import pandas as pd 
from datetime import datetime

class CentroidImage(object):
    
    image = ""
    brigthMin = 0
    NameCatalog = ""
    
    def __init__(self, _image, brigthMin=250):
        self.image=_image
        self.brigthMin = brigthMin
        
    def get_Image(self):
        return self.image

    def find_ListCentroid(self, ListRoid):
        ListCoord=[]
        for roid in ListRoid['rois']:
            ListCoord.append(self.find_Centroid(roid))
        df=pd.DataFrame(ListCoord)
        return df

    def setNameCatalog(self):
        self.NameCatalog = 'CatalogCentroid_'+datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]+'.dat'
    
    def getNameCatalog(self):
        return self.NameCatalog

    def find_Centroid(self,coord):
        x1, y1, x2, y2 = coord
        color=[0,0,0]
        CenterX = 0
        CenterY = 0
        for y in range(y1,y2):
            for x in range(x1,x2):
                if(np.average(self.image[x][y])>np.average(color)):
                    color = self.image[x][y]
                    CenterX = x
                    CenterY = y
        return [CenterY,CenterX,color]   
            
    def outPutFileImage(self,image):
        out_file=self.outPutFile
        image.save(out_file,'JPEG')        
        display(Image.open(out_file))
        
    def CreateCatalog(self,df,r,PathFile):
        self.setNameCatalog()
        data = Table({'#x': df[0],'y': df[1],'brightness':df[2],'class': r['class_ids'] ,'Prob': r['scores']},names=['#x','y','brightness','class','Prob'])
        ascii.write(data, PathFile, format='fixed_width', delimiter=None)
  