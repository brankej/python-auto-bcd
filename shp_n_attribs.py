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
This Script attempts to autmomatically detect bomb craters - MAIN Execute File
Created on Wed May 23 2018
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

args = parser.parse_args()


input = args.rast
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

#print stats_depth
####RASTERSTATS#######


data = gpd.read_file("output/craters_poly.shp")



count = 0
    # Empty column for area
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
    #print "index", index, "row", row
    # Update the value in 'area' column with area information at index
    data.loc[index, 'area'] = Area =row['geometry'].area
    data.loc[index, 'perimeter'] = Perimter  =(row['geometry']).length

    data.loc[index, 'compactn'] = Compactness = compactness(Perimter, Area)
    data.loc[index, 'circ'] = Compact_circ = compact_circ(Perimter, Area)

    #add depth value for index (int) to gpd dataframe
    data.loc[index, 'Depth'] = stats_depth[index]

    ####################
    #SELECT FOR SPECIFIC Values
    ####################

    #test true
    if data.loc[index, 'area'] > 12 and data.loc[index, 'area'] < 80 and data.loc[index, 'circ'] > 1.0 and data.loc[index, 'circ'] < 2.1:
         count +=1
         #print 'Treffer -->',count, data.loc[index, 'FID']
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
