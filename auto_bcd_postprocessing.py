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
This Script attempts to autmomatically detect past bomb craters - POSTPROCESSING
Created on Wed Juni 06 2018
@author: j.branke & j.köck
"""

#IMPORT MODULES=============================================================
import numpy as np
from math import *
from progress.bar import Bar
import argparse
import osgeo.gdal as gdal
import cv2 as cv
#===========================================================================


#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters - POSTPROCESSING.')
parser.add_argument('-input_craters', type=str, help='Input of bcd - Craters')
parser.add_argument('-input_edges', type=str, help='Input of bcd - Edges')


args = parser.parse_args()


input_craters = args.input_craters
input_edges = args.input_edges

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

#read in craters
craters_array = raster2array(input_craters)

#read in edges
edges_array = raster2array(input_edges)

###########get necessary raster information###########
myrast = gdal.Open(input_craters)
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

# ###DO STUFF
#
#
# ###Output
#
# #array_out
# driver = gdal.GetDriverByName('GTiff')
# dataset = driver.Create("output/bcd_raster.tif", NROWS, NCOLS, 1, gdal.GDT_Float32 )
# dataset.SetGeoTransform((XULCorner,Cellsize,0,YULCorner,0,-Cellsize))
# dataset.SetProjection(wkt_projection)
#
# band_1 = dataset.GetRasterBand(1)
# band_1.WriteArray(detect_array)
#
#
#
#
# #flushcache
# dataset.FlushCache()




print " --- done --- "
