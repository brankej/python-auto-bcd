# -*- coding: utf-8 -*-

  ###############################################################################
  ##
  ##  This program is free software: you can redistribute it and/or modify
  ##  it under the terms of the GNU General Public License as published by
  ##  the Free Software Foundation, either version 3 of the License, or
  ##  (at your option) any later version.
  ##
  ##  This program is distributed in the hope that it will be useful,
  ##  but WITHOUT ANY WARRANTY; without even the implied warranty of
  ##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  ##  GNU General Public License for more details.
  ##
  ##  You should have received a copy of the GNU General Public License
  ##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
  ##
  ###############################################################################


"""
This Script attempts to autmomatically detect past bomb craters - CALCULATION
Created on Fr June 22 2018
@author: j.branke & j.köck
"""

#IMPORT MODULES=============================================================
import numpy as np
from math import *
from progress.bar import Bar
import argparse
import osgeo.gdal as gdal
#===========================================================================

#PARSER====================================================================
parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters - CALCULATION.')
parser.add_argument('-input_svf', type=str, help='Input of sky-view-factor')
parser.add_argument('-input_minic', type=str, help='Input of morph_features -> minic')
parser.add_argument('-input_maxic', type=str, help='Input of morph_features -> maxic')
parser.add_argument('-input_profc', type=str, help='Input of profc')
parser.add_argument('-input_crosc', type=str, help='Input of crosc')
parser.add_argument('-input_pos', type=str, help='Input of pos')
parser.add_argument('-input_protection', type=str, help='Input of protection')
parser.add_argument('-input_curv_class', type=str, help='Input of curvature classes')

### # ### # ### # ###
parser.add_argument('-svf_thres_min', type=float, help='Threshold min SVF')
parser.add_argument('-svf_thres_max', type=float, help='Threshold max SVF')
parser.add_argument('-minic_thres_min', type=float, help='Threshold min MINIC')
parser.add_argument('-minic_thres_max', type=float, help='Threshold max MINIC')
parser.add_argument('-maxic_thres_min', type=float, help='Threshold min MAXIC')
parser.add_argument('-maxic_thres_max', type=float, help='Threshold max MAXIC')
parser.add_argument('-profc_thres_min', type=float, help='Threshold min PROFC')
parser.add_argument('-profc_thres_max', type=float, help='Threshold max PROFC')
parser.add_argument('-crosc_thres_min', type=float, help='Threshold min CROSC')
parser.add_argument('-crosc_thres_max', type=float, help='Threshold max CROSC')
parser.add_argument('-pos_thres_min', type=float, help='Threshold min POS')
parser.add_argument('-pos_thres_max', type=float, help='Threshold max POS')
parser.add_argument('-protection_thres_min', type=float, help='Threshold min PROTECTION')
parser.add_argument('-protection_thres_max', type=float, help='Threshold max PROTECTION')

args = parser.parse_args()

input_svf = args.input_svf
input_minic=args.input_minic
input_maxic=args.input_maxic
input_profc=args.input_profc
input_crosc=args.input_crosc
input_pos=args.input_pos
input_protection=args.input_protection
input_curv_class=args.input_curv_class

### # ### # ### # ###
thres_svf_min = args.svf_thres_min
thres_svf_max = args.svf_thres_max
thres_minic_min = args.minic_thres_min
thres_minic_max = args.minic_thres_max
thres_maxic_min = args.maxic_thres_min
thres_maxic_max = args.maxic_thres_max
thres_profc_min = args.profc_thres_min
thres_profc_max = args.profc_thres_max
thres_crosc_min = args.crosc_thres_min
thres_crosc_max = args.crosc_thres_max
thres_pos_min = args.pos_thres_min
thres_pos_max = args.pos_thres_max
thres_protection_min = args.protection_thres_min
thres_protection_max = args.protection_thres_max
#=========================================================================

########################################################
####             Functions                ##############
########################################################
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array

def thresholds2array(inarray, thresmin, thresmax, NCOLS, NROWS):
    """Select from Array(a) all values between specified threshold, returns binary array """
    outarray = np.empty((NCOLS,NROWS),dtype=float)
    for i in range(0,NCOLS,1):
         for j in range(0,NROWS,1):
             if inarray[i][j] > thresmin and inarray[i][j] < thresmax:
                 outarray[i][j] = 1
             else :
                 outarray[i][j] = 0
    return outarray

########################################################
####             Main                ###################
########################################################

#####
###EINLESEN
#####

#read in svf
svf_array = raster2array(input_svf)

#read in minic
minic_array = raster2array(input_minic)

#read in maxic
maxic_array = raster2array(input_maxic)

#read in profc
profc_array = raster2array(input_profc)

#read in crosc
crosc_array = raster2array(input_crosc)

#read in pos
pos_array = raster2array(input_pos)

#read in PROTECTION
protection_array = raster2array(input_protection)

#read in curv_class
class_array = raster2array(input_curv_class)

###########get necessary raster information###########
myrast = gdal.Open(input_minic)
NROWS = myrast.RasterXSize
NCOLS = myrast.RasterYSize
geotransform = myrast.GetGeoTransform()
wkt_projection = myrast.GetProjection()
XULCorner = geotransform[0]
YULCorner = geotransform[3]
Cellsize = geotransform[1]

myband = myrast.GetRasterBand(1)
Nodata = myband.GetNoDataValue()

print "--- DATA LOADED ---"         # TODO: unterschiedliche gewichtung der detect arrays

###DO STUFF
###########################################
svf_detect_array = np.empty((NCOLS,NROWS),dtype=float)
#####
bar = Bar(' -> Processing svf', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if svf_array[i][j] > thres_svf_min and svf_array[i][j] < thres_svf_max:
            svf_detect_array[i][j] = 1
        else :
            svf_detect_array[i][j] = 0

    bar.next()
bar.finish()

###########################################
minic_detect_array = np.empty((NCOLS,NROWS),dtype=float)
#####
bar = Bar(' -> Processing minic', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if minic_array[i][j] > thres_minic_min and minic_array[i][j] < thres_minic_max:
            minic_detect_array[i][j] = 1
        else :
            minic_detect_array[i][j] = 0

    bar.next()
bar.finish()

###########################################
maxic_detect_array = np.empty((NCOLS,NROWS),dtype=float)
#####
bar = Bar(' -> Processing maxic', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if maxic_array[i][j] > thres_maxic_min and maxic_array[i][j] < thres_maxic_max:
            maxic_detect_array[i][j] = 1
        else :
            maxic_detect_array[i][j] = 0

    bar.next()
bar.finish()

###########################################
class_detect_array = np.empty((NCOLS,NROWS),dtype=float)
#####
bar = Bar(' -> Processing curvature class', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if class_array[i][j] == 0:
            class_detect_array[i][j] = 1
        else :
            class_detect_array[i][j] = 0

    bar.next()
bar.finish()

#####EXTENDED#####

#############################################
profc_detect_array = np.empty((NCOLS,NROWS),dtype=float)
#####
bar = Bar(' -> Processing profc', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if profc_array[i][j] > thres_profc_min and profc_array[i][j] < thres_profc_max:
            profc_detect_array[i][j] = 1
        else :
            profc_detect_array[i][j] = 0

    bar.next()
bar.finish()

#############################################
crosc_detect_array = np.empty((NCOLS,NROWS),dtype=float)
#####
bar = Bar(' -> Processing crosc', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if crosc_array[i][j] > thres_crosc_min and crosc_array[i][j] < thres_crosc_max:
            crosc_detect_array[i][j] = 1
        else :
            crosc_detect_array[i][j] = 0

    bar.next()
bar.finish()

#############################################
pos_detect_array = np.empty((NCOLS,NROWS),dtype=float)

#####
bar = Bar(' -> Processing pos', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if pos_array[i][j] > thres_pos_min and pos_array[i][j] < thres_pos_max:
            pos_detect_array[i][j] = 1
        else :
            pos_detect_array[i][j] = 0

    bar.next()
bar.finish()

#############################################
protection_detect_array = np.empty((NCOLS,NROWS),dtype=float)

#####
bar = Bar(' -> Processing Protection', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if protection_array[i][j] > thres_protection_min and protection_array[i][j] < thres_protection_max:
            protection_detect_array[i][j] = 1
        else :
            protection_detect_array[i][j] = 0

    bar.next()
bar.finish()

####EXTENDED END#####

#############################################
detect_array = np.empty((NCOLS,NROWS),dtype=float)


#####
bar = Bar(' -> Processing Layerstack', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        detect_array[i][j]=svf_detect_array[i][j]+minic_detect_array[i][j]+class_detect_array[i][j]+maxic_detect_array[i][j]+profc_detect_array[i][j]+crosc_detect_array[i][j]+pos_detect_array[i][j]+protection_array[i][j]

    bar.next()
bar.finish()

#######################################
###Output

#detect_array_out
driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create("output/bcd_raster.tif", NROWS, NCOLS, 1, gdal.GDT_Float32 )
dataset.SetGeoTransform((XULCorner,Cellsize,0,YULCorner,0,-Cellsize))
dataset.SetProjection(wkt_projection)

band_1 = dataset.GetRasterBand(1)
band_1.WriteArray(detect_array)

#flushcache
dataset.FlushCache()

print " --- done --- "
