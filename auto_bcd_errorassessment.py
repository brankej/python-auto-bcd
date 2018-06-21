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
This Script attempts to autmomatically detect past bomb craters - PREPROCESSING
Created on Wed May 23 2018
@author: j.branke & j.köck
"""

#IMPORT MODULES=============================================================
import argparse
import numpy as np
import os
from osgeo import gdal
from osgeo import ogr
from sklearn import metrics
#===========================================================================



#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters - PREPROCESSING.')
parser.add_argument('-validation', type=str, help='Pfad zu den Validation Polygonshapefile')
parser.add_argument('-classified', type=str, help='Pfad zu den Klassifiziertem Polygonshapefile')

args = parser.parse_args()

val_shapefile = args.validation
classified = args.classified
#=========================================================================

########################################################
####             Functions                ##############
########################################################

def create_mask_from_vector(vector_data_path, cols, rows, geo_transform, projection, target_value=1):
    """Rasterrize the given vector - return datasoure (wrapper for gdal.RasterizerLayer)."""
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(vector_data_path, 0)
    layer = data_source.GetLayer(0)
    driver = gdal.GetDriverByName("MEM") # in memory dataset
    target_ds = driver.Create('', cols, rows, 1, gdal.GDT_UInt16)
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(projection)
    gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[target_value])
    return target_ds

def create_mask_from_vector_ext(vector_data_path, cols, rows, geo_transform, projection, target_value=1):
    """Rasterrize the given vector - return raster (wrapper for gdal.RasterizerLayer)."""
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(vector_data_path, 0)
    #check for datapath and rm
    if vector_data_path.startswith("data_input"):
        n = vector_data_path[10:-4]
    if vector_data_path.startswith("output"):
        n = vector_data_path[6:-4]
    # make raster
    name = "output%s_RAST.tif" % (n)
    layer = data_source.GetLayer(0)
    driver = gdal.GetDriverByName("GTiff") # in memory dataset
    target_ds = driver.Create(name, cols, rows, 1, gdal.GDT_UInt16)
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(projection)
    gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[target_value])


def vectors_to_raster(path, rows, cols, geo_transform, projection):
    """Rasterize vector"""
    labeled_pixels = np.zeros((rows, cols))
    label = 1
    ds= create_mask_from_vector(path, cols, rows, geo_transform, projection, target_value=label)
    #create bkp Raster of Output Data
    create_mask_from_vector_ext(path, cols, rows, geo_transform, projection, target_value=label)
    band = ds.GetRasterBand(1)
    labeled_pixels = band.ReadAsArray()
    ds=None
    return labeled_pixels


########################################################
####             Main                ###################
########################################################

raster_dataset = gdal.Open("output/closing.tif", gdal.GA_ReadOnly)
geo_transform = raster_dataset.GetGeoTransform()
proj = raster_dataset.GetProjectionRef()

band_1 = raster_dataset.GetRasterBand(1)
band_1_array = band_1.ReadAsArray()
rows, cols = band_1_array.shape

#ERROR ASSESSMENT

#shp output to raster to array
validat = vectors_to_raster(val_shapefile, rows, cols, geo_transform, proj)
predict = vectors_to_raster(classified, rows, cols, geo_transform, proj)

#to 1D array
validation_labels = validat.ravel()
predicted_labels = predict.ravel()

##ErrorAssessment Prints#
print " --- - --- "
print("Confussion matrix:\n%s" % metrics.confusion_matrix(validation_labels, predicted_labels))
print " --- - --- "
print("Classification report:\n%s" % metrics.classification_report(validation_labels, predicted_labels))
print " --- - --- "
print("Classification accuracy: \n ---> %f" % metrics.accuracy_score(validation_labels, predicted_labels))
print " --- - --- "
print("Classification Cohen's Kappa Value: \n ---> %f" % metrics.cohen_kappa_score(validation_labels, predicted_labels)) #https://de.wikipedia.org/wiki/Cohens_Kappa
print " --- - --- "
print("Classification R^2 (coefficient of determination): \n ---> %f" % metrics.r2_score(validation_labels, predicted_labels))
print " --- - --- "


print " --- done --- "
