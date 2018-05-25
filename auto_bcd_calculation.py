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
Created on Wed May 23 2018
@author: j.branke & j.köck
"""

#IMPORT MODULES=============================================================
import os
import numpy as np
from math import *
from progress.bar import Bar
import argparse
#===========================================================================


#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters.')
parser.add_argument('-input_svf', type=str, help='Input of sky-view-factor')
parser.add_argument('-input_minic', type=str, help='Input of morph_features -> minic')
parser.add_argument('-input_sinks', type=str, help='Input of sinks')
#parser.add_argument('-output', type=str, help='Output of detected points of interest')
#parser.add_argument('-size', type=int, help='size for further calculations', nargs='?', default=9)
#parser.add_argument('-method', type=str, help='method for calculations', choices=['all','skyview','morph_features','sinks'])

args = parser.parse_args()


input_svf = args.input_svf
input_minic=args.input_minic
input_sinks=args.input_sinks
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
    return arrays

def coord2pixelOffset(rasterfn,x,y):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    xOffset = int((x - originX)/pixelWidth)
    yOffset = int((y - originY)/pixelHeight)
    return xOffset,yOffset

def pixelOffset2coord(rasterfn,xOffset,yOffset):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    coordX = originX+pixelWidth*xOffset
    coordY = originY+pixelHeight*yOffset
    return coordX, coordY



########################################################
####             Main                ###################
########################################################







###layerstack sum###
#os.system('saga_cmd grid_calculus.so 1 -GRIDS [tmp/svf_1.sgrd, tmp/minic_1.sgrd, tmp/sinks_1.sgrd] -RESULT rast_calc_result.sgrd -FORMULA "(g1 + g2 + g3)" -TYPE 8')

#os.system('saga_cmd grid_tools 15  -> reclassify -> export to shp


print " --- done --- "
