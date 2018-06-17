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
import osgeo.ogr as ogr
import cv2 as cv
import geopandas as gpd
#===========================================================================


#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters - POSTPROCESSING.')
parser.add_argument('-input_craters', type=str, help='Input of bcd - Craters')
parser.add_argument('-thresmax', type=float, help='max threshold for bombcraters value' , nargs='?', default= 8)
parser.add_argument('-thresmin', type=float, help='min threshold for bombcraters value', nargs='?', default= 4.2)
parser.add_argument('-kernel', type=int, help='Kernel Size', nargs='?', default= 3)



args = parser.parse_args()


input_craters = args.input_craters
thresmax = args.thresmax
thresmin = args.thresmin
kernel = args.kernel
#=========================================================================


########################################################
####             Functions                ##############
########################################################

def raster2array(rasterfn):
    """Input Raster to Array """
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

def segments(poly):
        """A sequence of (x,y) numeric coordinates pairs """
        return zip(poly, poly[1:] + [poly[0]])

def area_(poly):
    """A sequence of (x,y) numeric coordinates pairs """
    return 0.5 * abs(sum(x0*y1 - x1*y0
        for ((x0, y0), (x1, y1)) in segments(poly)))

def perimeter_(poly):
    """A sequence of (x,y) numeric coordinates pairs """
    return abs(sum(math.hypot(x0-x1,y0-y1) for ((x0, y0), (x1, y1)) in segments(poly)))

def compactness(Perimeter, Area):
    """Calculation of Compactness Values"""
    compactness = Perimeter / (2 * sqrt(PI * Area))
    return compactness

def frac_dim(Perimeter, Area):
    """Calculation of Fractal Dimensions"""
    fracdim = 2 * (log(Perimeter) / log(Area))
    return fracdim

########################################################
####             Main                ###################
########################################################


###EINLESEN

#read in craters
craters_array = raster2array(input_craters)


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

########################
#to binary
########################
bombcraters_array = thresholds2array(craters_array, thresmin, thresmax, NCOLS, NROWS)

driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create("output/bombcraters.tif", NROWS, NCOLS, 1, gdal.GDT_Float32 )
dataset.SetGeoTransform((XULCorner,Cellsize,0,YULCorner,0,-Cellsize))
dataset.SetProjection(wkt_projection)

band_1 = dataset.GetRasterBand(1)
band_1.WriteArray(bombcraters_array)

# morphological transformation                                             #https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html

#opening
kernel = np.ones((kernel,kernel),np.uint8)
opening = cv.morphologyEx(bombcraters_array, cv.MORPH_OPEN, kernel)

driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create("output/opening.tif", NROWS, NCOLS, 1, gdal.GDT_Float32 )
dataset.SetGeoTransform((XULCorner,Cellsize,0,YULCorner,0,-Cellsize))
dataset.SetProjection(wkt_projection)

band_1 = dataset.GetRasterBand(1)
band_1.WriteArray(opening)

#closing
closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

driver = gdal.GetDriverByName('GTiff')
dataset = driver.Create("output/closing.tif", NROWS, NCOLS, 1, gdal.GDT_Float32 )
dataset.SetGeoTransform((XULCorner,Cellsize,0,YULCorner,0,-Cellsize))
dataset.SetProjection(wkt_projection)

band_1 = dataset.GetRasterBand(1)
band_1.WriteArray(closing)


#flushcache
dataset.FlushCache()

########################################################################

#############
#POLYGONIZE
#############
#  get raster datasource
src_ds = gdal.Open("output/closing.tif")
srcband = src_ds.GetRasterBand(1)
#  create output datasource

dst_layername = "output/craters_poly"
drv = ogr.GetDriverByName("ESRI Shapefile")
dst_ds = drv.CreateDataSource( dst_layername + ".shp" )
dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
gdal.Polygonize( srcband, srcband , dst_layer, -1, [], callback=None )

print "--- Polygonize done ---"
########################################################################

#############
#Calc GEOMETRY
#############
# Read file using read_file
data = gpd.read_file("output/craters_poly.shp")

#We can iterate over the selected rows using a specific .iterrows() -function in (geo)pandas:
#for index, row in data.iterrows():
    #poly_area = row['geometry'].area
    #print("Polygon area at index {0} is: {1:.3f}".format(index, poly_area))

# Iterate rows one at the time
for index, row in data.iterrows():
    # Empty column for area
    data['area'] = None
    data['perimeter'] = None
    data['compactn'] = None
    data['fracdim'] = None

    # Update the value in 'area' column with area information at index
    data.loc[index, 'area'] = area_(row['geometry'])
    data.loc[index, 'perimeter'] = perimeter_(row['geometry'])
    data.loc[index, 'compactn'] = compactness(row['perimeter'],row['area'])
    data.loc[index, 'fracdim'] = frac_dim(row['perimeter'],row['area'])

# Maximum area # Minimum area
max_area = data['area'].max()
min_area = data['area'].mean()
print("Max area: %s\nMean area: %s" % (round(max_area, 2), round(min_area, 2)))



####################
#SELECT FOR SPECIFIC Values
####################

# Create a output path for the data
outpoly = "output/craters_poly_w_data.shp"
# Write those rows into a new Shapefile (the default output file format is Shapefile)
data.to_file(outpoly)


print " --- done --- "
