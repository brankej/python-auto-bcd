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
#===========================================================================



#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters - PREPROCESSING.')
parser.add_argument('-DEM', type=str, help='Input of digital elevation model')

 # TODO: in help cite authors of ideas and tools

args = parser.parse_args()


input = args.DEM
#=========================================================================

########################################################
####             Functions                ##############
########################################################



########################################################
####             Main                ###################
########################################################



print " --- done --- "
