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
import os
import argparse
from progress.spinner import Spinner
#===========================================================================



#PARSER====================================================================

parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect bomb craters - MAIN Execute File.')
parser.add_argument('-DEM', type=str, help='Input of digital elevation model')
parser.add_argument('-size', type=int, help='size for further calculations', nargs='?', default=9)
parser.add_argument('-method', type=str, help='method for calculations --> List of Different SAGA GIS Tools containing (SVF; MINIC; MAXIC; PROFC; CROSC; CLASS; SINKS; T.OPENESS [optional TPI])', choices=['less','all'], nargs='?', default='less')
parser.add_argument('-pre', type=str, help='pre of preprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')
parser.add_argument('-calc', type=str, help='calc of preprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')
parser.add_argument('-post', type=str, help='post of postprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')
parser.add_argument('-error', type=str, help='post of postprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')

args = parser.parse_args()


input = args.DEM
size=args.size
method=args.method
pre=args.pre
calc=args.calc
post=args.post#
error=args.error
#=========================================================================


########################################################
####             Functions                ##############
########################################################



########################################################
####             Main                ###################
########################################################

#OUTPUT===================================================================

#####PREPROCESSING########
spinner = Spinner('Loading ')
state = "Running"
while state != 'FINISHED':
    # Do some work

    if pre=="TRUE":
        cmd ="python auto_bcd_preprocessing.py -DEM %s -method %s -size %i " %(input, method, size)
        os.system(cmd)

        print " --- Preprocessing completed --- "
        spinner.next()
        state = "FINISHED"
    else:
        print "skipped Preprocessing"
        spinner.next()
        state = "FINISHED"

print " --- done --- "
    ###################################

#####CALCULATION########
spinner = Spinner('Loading ')
state = "Running"
while state != 'FINISHED':
    # Do some work
    if calc=="TRUE":
        cmd ="python auto_bcd_calculation.py -input_svf tmp/svf.sdat -input_minic tmp/minic.sdat -input_maxic tmp/maxic.sdat -input_profc tmp/profc.sdat -input_crosc tmp/crosc.sdat -input_curv_class tmp/class.sdat -input_pos tmp/pos.sdat -input_protection tmp/protection.sdat" #-input_sinks tmp/sinks.sdat
        os.system(cmd)

        print " --- Calculations completed --- "
        spinner.next()
        state = "FINISHED"

    else:
        print "skipped Calculation"
        spinner.next()
        state = "FINISHED"

print " --- done --- "

    ###################################

#####POSTPROCESSING#####
spinner = Spinner('Loading ')
state = "Running"
while state != 'FINISHED':
    # Do some work

    if post=="TRUE":
        cmd ="python auto_bcd_postprocessing.py -input_craters output/bcd_raster.tif"
        os.system(cmd)

        cmd="python shp_n_attribs.py -rast data_input/%s" % (input)
        os.system(cmd)

        print " --- Postprocessing completed --- "
        spinner.next()
        state = "FINISHED"

    else:
        print "skipped Postprocessing"
        spinner.next()
        state = "FINISHED"

print " --- done --- "

    ###################################

#####ERROR ASSESSMENT#####
spinner = Spinner('Loading ')
state = "Running"
while state != 'FINISHED':
    # Do some work

    if error =="TRUE":
        cmd ="python auto_bcd_errorassessment.py -validation data_input/XYXYX.shp" # TODO: !!!!!!!
        os.system(cmd)

        print " --- Error Assessment completed --- "
        spinner.next()
        state = "FINISHED"

    else:
        print "skipped Error Assessment"
        spinner.next()
        state = "FINISHED"

print " --- done --- "

print " --- Automatic Bomb Crate Detection FINISHED --- "
