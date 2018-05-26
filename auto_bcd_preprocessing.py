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
parser.add_argument('-input_dem', type=str, help='Input of digital elevation model')
#parser.add_argument('-output', type=str, help='Output of detected points of interest')
parser.add_argument('-size', type=int, help='size for further calculations', nargs='?', default=9)
parser.add_argument('-method', type=str, help='method for calculations', choices=['all','skyview','minic','sinks'], nargs='?', default='all')

args = parser.parse_args()


input = args.input_dem
#output=args.output
size=args.size
method=args.method
#=========================================================================



########################################################
####             Functions                ##############
########################################################



########################################################
####             Main                ###################
########################################################




if method=="skyview":
    cmd ='saga_cmd ta_lighting 3 -DEM data_input/%s -SVF tmp/svf.sgrd -VISIBLE tmp/visible.sgrd' %(input)
    os.system(cmd)

elif method=="minic":
    cmd ='saga_cmd ta_morphometry 23 -DEM data_input/%s -FEATURES tmp/features.sgrd -MINIC tmp/minic.sgrd -SIZE %i' %(input, size)
    os.system(cmd)

elif method=="sinks":
    cmd ='saga_cmd sim_qm_of_esp 1 -DEM data_input/%s -FILLED tmp/filledsinks.sgrd -SINKS tmp/sinks.sgrd -DZFILL 0.05' %(input)
    os.system(cmd)

elif method=="all":
    cmd ='saga_cmd ta_lighting 3 -DEM data_input/%s -SVF tmp/svf.sgrd -VISIBLE tmp/visible.sgrd' %(input)
    os.system(cmd)

    cmd ='saga_cmd ta_morphometry 23 -DEM data_input/%s -FEATURES  tmp/features.sgrd -MINIC tmp/minic.sgrd -SIZE %i' %(input, size)
    os.system(cmd)

    cmd ='saga_cmd sim_qm_of_esp 1 -DEM data_input/%s -FILLED  tmp/filledsinks.sgrd -SINKS tmp/sinks.sgrd -DZFILL 0.05' %(input)
    os.system(cmd)


print " --- done --- "
