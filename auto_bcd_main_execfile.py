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
Created on Fr June 22 2018
@author: j.branke & j.köck
"""

#IMPORT MODULES=============================================================
import os
import argparse
from datetime import datetime as dt
#===========================================================================

#PARSER====================================================================
parser = argparse.ArgumentParser(description='This Script attempts to autmomatically detect bomb craters - MAIN Execute File.')
parser.add_argument('-DEM', type=str, help='Input of digital elevation model')
parser.add_argument('-thres', type=str, help='Input of Thresholds.txt File')
parser.add_argument('-vali', type=str, help='Input of validation Shapefile',nargs='?', default=None)
parser.add_argument('-size', type=int, help='size for further calculations', nargs='?', default=9)
parser.add_argument('-method', type=str, help='method for calculations --> List of Different SAGA GIS Tools containing (SVF; Openess; Protection Index [less]; MINIC; MAXIC; PROFC; CROSC; CLASS [all])', choices=['less','all'], nargs='?', default='less')
parser.add_argument('-pre', type=str, help='pre of preprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')
parser.add_argument('-calc', type=str, help='calc of preprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')
parser.add_argument('-post', type=str, help='post of postprocessing tool usage', choices=['TRUE','FALSE'], nargs='?', default='TRUE')
parser.add_argument('-error', type=str, help='error of error assessment tool usage', choices=['TRUE','FALSE'], nargs='?', default='FALSE')

args = parser.parse_args()

input = args.DEM
thres = args.thres
vali = args.vali
size=args.size
method=args.method
pre=args.pre
calc=args.calc
post=args.post
error=args.error
#=========================================================================

########################################################
####             Functions                ##############
########################################################

########################################################
####             Main                ###################
########################################################
start = dt.now()

with open("data_input/"+thres, "r") as fobj:
    lines = fobj.readlines()[2:] #skip header
    for line in lines:
        #print line
        line = line.strip()
        line = line.split(";")

        thres_svf_min = float(line[0])
        thres_svf_max = float(line[1])
        thres_minic_min = float(line[2])
        thres_minic_max = float(line[3])
        thres_maxic_min = float(line[4])
        thres_maxic_max = float(line[5])
        thres_profc_min = float(line[6])
        thres_profc_max = float(line[7])
        thres_crosc_min = float(line[8])
        thres_crosc_max = float(line[9])
        thres_pos_min = float(line[10])
        thres_pos_max = float(line[11])
        thres_protection_min = float(line[12])
        thres_protection_max = float(line[13])
        thres_detect_min = float(line[14])
        thres_detect_max =  float(line[15])
        kernel_size = int(line[16])
        thres_area_min = float(line[17])
        thres_area_max = float(line[18])
        thres_circ_min = float(line[19])
        thres_circ_max = float(line[20])

fobj.close()
#OUTPUT===================================================================

#####PREPROCESSING########
if pre=="TRUE":
    cmd ="python auto_bcd_preprocessing.py -DEM %s -method %s -size %i " %(input, method, size)
    os.system(cmd)

    print " --- Preprocessing completed --- "

else:
    print "skipped Preprocessing"

print " --- done --- "
    ###################################

#####CALCULATION########
# Do some work
if calc=="TRUE" and method=="all":
    cmd ="python auto_bcd_calculation.py -method %s -input_svf tmp/svf.sdat -input_minic tmp/minic.sdat -input_maxic tmp/maxic.sdat -input_profc tmp/profc.sdat -input_crosc tmp/crosc.sdat -input_curv_class tmp/class.sdat -input_pos tmp/pos.sdat -input_protection tmp/protection.sdat -svf_thres_min %f -svf_thres_max %f -minic_thres_min %f -minic_thres_max %f -maxic_thres_min %f -maxic_thres_max %f -profc_thres_min %f -profc_thres_max %f -crosc_thres_min %f -crosc_thres_max %f -pos_thres_min %f -pos_thres_max %f -protection_thres_min %f -protection_thres_max %f " % (method, thres_svf_min, thres_svf_max, thres_minic_min , thres_minic_max, thres_maxic_min, thres_maxic_max, thres_profc_min, thres_profc_max, thres_crosc_min, thres_crosc_max, thres_pos_min, thres_pos_max, thres_protection_min, thres_protection_max)
    os.system(cmd)

    print " --- Calculations completed --- "

if calc=="TRUE" and method=="less":
    cmd ="python auto_bcd_calculation.py -method %s -input_svf tmp/svf.sdat -input_pos tmp/pos.sdat -input_protection tmp/protection.sdat -svf_thres_min %f -svf_thres_max %f -pos_thres_min %f -pos_thres_max %f -protection_thres_min %f -protection_thres_max %f " % (method, thres_svf_min, thres_svf_max, thres_pos_min, thres_pos_max, thres_protection_min, thres_protection_max)
    os.system(cmd)

    print " --- Calculations completed --- "

else:
    print "skipped Calculation"

print " --- done --- "

    ###################################

#####POSTPROCESSING#####

if post=="TRUE":
    cmd ="python auto_bcd_postprocessing.py -input_craters output/bcd_raster.tif -kernel %i -thresmin %f -thresmax %f" % (kernel_size, thres_detect_min, thres_detect_max)
    os.system(cmd)

    cmd="python auto_bcd_shp_n_attribs.py -rast data_input/%s -area_thres_min %f -area_thres_max %f -circ_thres_min %f -circ_thres_max %f" % (input, thres_area_min, thres_area_max, thres_circ_min, thres_circ_max)
    os.system(cmd)

    print " --- Postprocessing completed --- "

else:
    print "skipped Postprocessing"

print " --- done --- "

    ###################################

#####ERROR ASSESSMENT#####

if error =="TRUE":
    cmd ="python auto_bcd_errorassessment.py -classified output/Treffer_shape.shp -validation data_input/%s " % (vali)# TODO: !!!!!!!
    os.system(cmd)

    print " --- Error-Assessment completed --- "

else:
    print "skipped Error-Assessment"

print " --- done --- "


#python auto_bcd_main_execfile.py -DEM DGM05_bombdetect_cut.tif -thres Thresholds.txt -vali bombcraters_validate_cut.shp -error TRUE
#python auto_bcd_main_execfile.py -DEM DGM05_bombdetect_cut_natters.tif -thres Thresholds.txt -vali bombcraters_validate_cut_natters.shp -error TRUE
#python auto_bcd_main_execfile.py -DEM uni_ALSNORDTIROL_DGM_1m_cut.tif -thres Thresholds.txt -vali bombcraters_validate_cut.shp -error TRUE

print " --- Automatic Bomb Crate Detection FINISHED --- "
print dt.now() - start
