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
Created on Wed May 23 2018
@author: j.branke & j.köck
"""

#IMPORT MODULES=============================================================
import os
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
parser.add_argument('-input_sinks', type=str, help='Input of sinks')
parser.add_argument('-input_curv_class', type=str, help='Input of curvature classes')
#parser.add_argument('-output', type=str, help='Output of detected points of interest')
#parser.add_argument('-size', type=int, help='size for further calculations', nargs='?', default=9)
#parser.add_argument('-method', type=str, help='method for calculations', choices=['all','skyview','morph_features','sinks'])

args = parser.parse_args()


input_svf = args.input_svf
input_minic=args.input_minic
input_sinks=args.input_sinks
input_curv_class=args.input_curv_class
#output=args.output
#size=args.size
#method=args.method
#=========================================================================


########################################################
####             Functions                ##############
########################################################
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array

########################################################
####             Main                ###################
########################################################


###EINLESEN

#read in svf

svf_array = raster2array(input_svf)


#read in sinks

sinks_array = raster2array(input_sinks)


#read in minic

minic_array = raster2array(input_minic)

#read in minic

class_array = raster2array(input_curv_class)


myrast = gdal.Open(input_sinks)
NROWS = myrast.RasterXSize
NCOLS = myrast.RasterYSize
geotransform = myrast.GetGeoTransform()
wkt_projection = myrast.GetProjection()
XULCorner = geotransform[0]
YULCorner = geotransform[3]
Cellsize = geotransform[1]

myband = myrast.GetRasterBand(1)
Nodata = myband.GetNoDataValue()

print "--- DATA LOADED ---"

###DO STUFF

svf_detect_array = np.empty((NCOLS,NROWS),dtype=float)

#####
bar = Bar(' -> Processing svf', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if svf_array[i][j] > 0.8 and svf_array[i][j] < 0.95:
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

        if minic_array[i][j] > -0.1 and minic_array[i][j] < 0.0:
            minic_detect_array[i][j] = 1
        else :
            minic_detect_array[i][j] = 0

    bar.next()
bar.finish()

###########################################
class_detect_array = np.empty((NCOLS,NROWS),dtype=float)

#####
bar = Bar(' -> Processing curvature class', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if class_array[i][j] = 0:
            class_detect_array[i][j] = 1
        else :
            class_detect_array[i][j] = 0

    bar.next()
bar.finish()

#############################################
sinks_detect_array = np.empty((NCOLS,NROWS),dtype=float)

#####
bar = Bar(' -> Processing sinks', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        if sinks_array[i][j] > 0.0 and sinks_array[i][j] < 3.0:
            sinks_detect_array[i][j] = 1
        else :
            sinks_detect_array[i][j] = 0

    bar.next()
bar.finish()


#############################################
detect_array = np.empty((NCOLS,NROWS),dtype=float)

#####
bar = Bar(' -> Processing Layerstack', max=NCOLS, suffix='%(percent)d%%')
######

for i in range(0,NCOLS,1):
    for j in range(0,NROWS,1):

        detect_array[i][j]=svf_detect_array[i][j]+minic_detect_array[i][j]+sinks_detect_array[i][j]+class_detect_array[i][j]

    bar.next()
bar.finish()
###Output

driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create("output/bcd_raster.tif", NROWS, NCOLS, 1, gdal.GDT_Float32 )
dataset.SetGeoTransform((XULCorner,Cellsize,0,YULCorner,0,-Cellsize))
dataset.SetProjection(wkt_projection)

band_1 = dataset.GetRasterBand(1)
band_1.WriteArray(detect_array)

dataset.FlushCache()


###layerstack sum###
#cmd ='saga_cmd grid_calculus.so 1 -GRIDS [tmp/svf_1.sgrd, tmp/minic_1.sgrd, tmp/sinks_1.sgrd] -RESULT rast_calc_result.sgrd -FORMULA "(g1 + g2 + g3)" -TYPE 8')
#os.system(cmd)
#os.system('saga_cmd grid_tools 15  -> reclassify -> export to shp


print " --- done --- "
