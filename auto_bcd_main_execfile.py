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
import argparse
#===========================================================================



#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect past bomb craters.')
parser.add_argument('-input_dem', type=str, help='Input of digital elevation model')
parser.add_argument('-output', type=str, help='Output of detected points of interest')
parser.add_argument('-size', type=int, help='size for further calculations', nargs='?', default=9)
parser.add_argument('-method', type=str, help='method for calculations', choices=['all','skyview','minic','sinks'], nargs='?', default='all')
parser.add_argument('-mode', type=str, help='mode of preprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')

args = parser.parse_args()


input = args.input_dem
output=args.output
size=args.size
method=args.method
mode=args.mode
#=========================================================================


########################################################
####             Functions                ##############
########################################################



########################################################
####             Main                ###################
########################################################

#OUTPUT===================================================================

if mode=="TRUE":
    os.system("python auto_bcd_preprocessing.py -input_dem %s -output %s -size %i -method %s -mode %s") %(input, output, size, method, mode)

    print " --- Preprocessing completed --- "

else:
    print "skipped Preprocessing"


#os.system("python auto_bcd_calculation.py -input_svf tmp/svf.sgrd -input_minic tmp/minic.sgrd -input_sinks tmp/sinks.sgrd")

print " --- Calculations completed --- "


print " --- done --- "