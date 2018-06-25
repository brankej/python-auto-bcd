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
This Script attempts to autmomatically detect bomb craters - Shape'n Attributes Script
Created on Fr June 22 2018
@author: j.branke & j.köck
"""

#IMPORT MODULES=============================================================
#import sys
#sys.path.append('''C:\Python27\Lib\site-packages\geopandas''')
import geopandas as gpd
from math import *
from rasterstats import zonal_stats
import argparse
from progress.bar import Bar

#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect bomb craters - Extended POSTPROCESSING.')
parser.add_argument('-rast', type=str, help='Input of Raster')
parser.add_argument('-area_thres_min', type=float, help='Threshold min Area', nargs='?', default= 12.0)
parser.add_argument('-area_thres_max', type=float, help='Threshold max Area', nargs='?', default= 80.0)
parser.add_argument('-circ_thres_min', type=float, help='Threshold min Circularity', nargs='?', default= 1.0)
parser.add_argument('-circ_thres_max', type=float, help='Threshold max Circularity', nargs='?', default= 2.1)

args = parser.parse_args()

input = args.rast
area_min = args.area_thres_min
area_max = args.area_thres_max
circ_min = args.circ_thres_min
circ_max = args.circ_thres_max
#=========================================================================

########################################################
####             Functions                ##############
########################################################

def compactness(Perimeter, Area):
    """Calculation of Compactness Values"""
    compactness = Perimeter / (2 * sqrt(pi * Area))
    return compactness

def compact_circ(Perimeter, Area):
    """Calculation of shape compactness for a circle"""
    compactcirc = ((Perimeter)**2 / (4*pi*Area))
    return compactcirc

########################################################
####             Main                ###################
########################################################

####RASTERSTATS#######
raster2stats="%s" % (input)
stats = zonal_stats("output/craters_poly.shp", raster2stats)

#empty container lists
stats_depth = []
stats_min = []
stats_max = []
stats_max_min = []

#get min and max from stats to list --> zip
stats_min = [s['min'] for s in stats]
stats_max = [s['max'] for s in stats]
stats_max_min = zip(stats_max, stats_min)

#calc depth for ziplist
for k in range(len(stats_max_min)):
    stats_depth.append(stats_max_min[k][0] - stats_max_min[k][1])

####Let the (Geo)Pandas Work#######

data = gpd.read_file("output/craters_poly.shp")

    # Empty columns
data['area'] = None
data['perimeter'] = None
data['compactn'] = None
data['circ'] = None
data['Depth'] = None
data['Treffer'] = None

#####
bar = Bar(' -> Creating Attrib Fields', max=len(data), suffix='%(percent)d%%')
######
# Iterate rows one at the time
for index, row in data.iterrows():
    # Update the value in 'area' column with area information at index
    data.loc[index, 'area'] = Area = row['geometry'].area
    data.loc[index, 'perimeter'] = Perimter = row['geometry'].length
    data.loc[index, 'compactn'] = Compactness = compactness(Perimter, Area)
    data.loc[index, 'circ'] = Compact_circ = compact_circ(Perimter, Area)
    #add depth value for index (int) to gpd dataframe
    data.loc[index, 'Depth'] = stats_depth[index]

    ####################
    #SELECT FOR parsed Values
    ####################
    #test true
    if data.loc[index, 'area'] > area_min and data.loc[index, 'area'] < area_max and data.loc[index, 'circ'] > circ_min and data.loc[index, 'circ'] < circ_max:
         data.loc[index, 'Treffer'] = 1

    bar.next()
bar.finish()

data[data['Treffer'] == 1].to_file('output/Treffer_shape.shp')

print "calc done"

# Create a output path for the data
outpoly = "output/craters_poly_w_data.shp"
# Write those rows into a new Shapefile (the default output file format is Shapefile)
data.to_file(outpoly)
#-------------------------------------------------------------------------------#

##EXTENDED##

print "--- done ---"
