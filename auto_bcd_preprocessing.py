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
Created on Fr June 22 2018
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
parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters - PREPROCESSING.')
parser.add_argument('-DEM', type=str, help='Input of digital elevation model')
parser.add_argument('-size', type=int, help='size for further calculations', nargs='?', default=9)
parser.add_argument('-method', type=str, help='method for calculations --> List of Different SAGA GIS Tools containing (SVF; MINIC; MAXIC; PROFC; CROSC; CLASS; SINKS; T.OPENESS [optional TPI] [https://github.com/brankej/python-auto-bcd])', choices=['less','all'], nargs='?', default='less')
parser.add_argument('-radius', type=int, help='radius of suspected bombcraters', nargs='?', default=5)


args = parser.parse_args()

input = args.DEM
size=args.size
method=args.method
radius=args.radius
#=========================================================================

########################################################
####             Functions                ##############
########################################################

########################################################
####             Main                ###################
########################################################

# TODO: check for time by specific tool -> most time expensive tool -> skyview

if method=="less":
    cmd ='saga_cmd ta_lighting 3 -DEM data_input/%s -SVF tmp/svf.sgrd -VISIBLE tmp/visible.sgrd' %(input)
    os.system(cmd)

    cmd = 'saga_cmd ta_lighting 5 -DEM data_input/%s -POS tmp/pos.sgrd -NEG tmp/neg.sgrd' %(input)
    os.system(cmd)

    cmd = 'saga_cmd ta_morphometry 7 -DEM data_input/%s -PROTECTION tmp/protection.sgrd -RADIUS %i' %(input, radius)
    os.system(cmd)

elif method=="all":
    cmd ='saga_cmd ta_lighting 3 -DEM data_input/%s -SVF tmp/svf.sgrd -VISIBLE tmp/visible.sgrd' %(input)
    os.system(cmd)

    cmd ='saga_cmd ta_morphometry 23 -DEM data_input/%s -FEATURES tmp/features.sgrd -MINIC tmp/minic.sgrd -MAXIC tmp/maxic.sgrd -PROFC tmp/profc.sgrd -CROSC tmp/crosc.sgrd -SIZE %i' %(input, size)
    os.system(cmd)

    cmd ='saga_cmd ta_morphometry 4 -DEM data_input/%s -CLASS tmp/class.sgrd' %(input)
    os.system(cmd)

    cmd = 'saga_cmd ta_lighting 5 -DEM data_input/%s -POS tmp/pos.sgrd -NEG tmp/neg.sgrd' %(input)
    os.system(cmd)

    cmd = 'saga_cmd ta_morphometry 7 -DEM data_input/%s -PROTECTION tmp/protection.sgrd -RADIUS %i' %(input, radius)
    os.system(cmd)

print " --- done --- "
