# python-auto-bcd

Library of Python-Scripts for automated detection of bomb craters on the foundation of a digital elevation model (DEM).

## Content

- auto_bcd_main_execfile[.py] --> Main Script
- auto_bcd_preprocessing[.py] --> Data Preprocessing
- auto_bcd_calculation[.py] --> First Selection on basis of preprocessed data
- auto_bcd_postprocessing[.py] --> Morphological Transformations, Polygonization
- auto_bcd_shp_n_attribs[.py] --> Calculation for Polygon Shp-File Attribut-Values
- auto_bcd_errorassessment[.py] --> Error - Assessment --> [TP, TN, FP, FN]

## Dependencies

- SAGA GIS with enabled Commandline Capabilities [http://www.saga-gis.org/en/index.html]

- scikit-learn [https://pypi.org/project/scikit-learn/]
- numpy [https://pypi.org/project/numpy/]
- progress [https://pypi.org/project/progress/]
- argparse [https://pypi.org/project/argparse/]
- gdal,ogr [https://pypi.org/project/GDAL/]
- opencv [https://pypi.org/project/opencv-python/]
- geopandas [https://pypi.org/project/geopandas/]
- rasterstats [https://pypi.org/project/rasterstats/]

## SAGA GIS Usage in Preprocessing

- Sky View factor O.Conrad (c) 2008 Ref.: Oke, T.R. (2000); Hantzschel et al. (2005); Boehner & Antonic (2009) [http://www.saga-gis.org/saga_tool_doc/2.2.3/ta_lighting_3.html]
- Morphometric Features O.Conrad (c) 2013 Ref.: Wood, J. (1996; 2009) [http://www.saga-gis.org/saga_tool_doc/2.2.7/ta_morphometry_23.html]
- Curvature Classification O.Conrad (c) 2001 Ref.: Dikau R. (1988) [http://www.saga-gis.org/saga_tool_doc/2.2.3/ta_morphometry_4.html]
- Morphometric Protection Index Victor Olaya (c) 2005 [http://www.saga-gis.org/saga_tool_doc/2.2.1/ta_morphometry_7.html]
- Topographic Openness O.Conrad (c) 2012 Ref.: Yokoyama et al. (2002); Prima et al. (2006); Anders et al. (2009) [http://www.saga-gis.org/saga_tool_doc/2.2.1/ta_lighting_5.html]

## Folder structure & data requirement

- data_input
  1. digital elevation model (DEM); best pixelsize < 5 meters
  2. [.txt] File with thresholds
  3. (optional) digitized bc shp-File for Error Assessment
- tmp
  - mainly preprocessing data will be saved there
- output
  - bcd_raster[.tif]
  - bombcraters[.tif]
  - opening[.tif]
  - closing[.tif]
  - validation_shp_RAST[.tif]
  - Treffer_shape_RAST[.tif]

  - Treffer_shape[.shp]
  - craters_poly[.shp]
  - craters_poly_w_data[.shp]

## still WIP

cheers
