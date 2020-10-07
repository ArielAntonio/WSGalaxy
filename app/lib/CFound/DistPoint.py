import math as m
import numpy as np
import pandas as pd
from scipy.spatial import distance
from astropy.io import fits as pyfits
from astropy.wcs import WCS
from astropy import units as u
from astropy.coordinates import SkyCoord

class CentroidImage(object):
    def getDistPoint(x_im, y_im, df, scale):
        x_im_center = x_im/2             #pixels
        y_im_center = y_im/2             #pixels
        #im_scale=0.360115  #arcsec/pixel
        #im_pixel=512       #pixels
        #im_size=184.38     #arcsec

        #df['dist'] = round(distance.euclidean([x_im_center, y_im_center, 0], [df['x'],df['y'], 0])) #pixels
        #dist_arcsec= dist* im_scale  #arcsec
        #print(dist_arcsec)
