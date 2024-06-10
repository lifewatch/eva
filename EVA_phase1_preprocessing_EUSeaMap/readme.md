# Converting a polygon map to hexagons(centers)

## About
- Use case: the EUNIS map information needs to be translated to match the hexagons of the BBT analysis.
- why python and not R: python geopandas is faster and more efficient when reading the polygon map.

## How to use

### Inputs
The process requires following datasets:
- map: the map to "path/to/source_map.gdb" (Euseamap downloaded from https://emodnet.ec.europa.eu/geoviewer/)
- hexagons = "path/to/shapefile_containing_hexagons.shp" (BBT hexagons)
- preprocessing = "path/to/write/preprocessed/data/directory" (output directory)

### Processing
See example in main.py script or main.ipynb.

### Outputs
- [basename_of_map]_clipped.shp: a .shp containing the map clipped to the extent of the hexagons.
- [basename_of_map]_hexagons.shp: a .shp containing the hexagonized map. 
- [basename_of_map]_hexagons.csv: a .csv containing the hexagonized map information without geodata. 

## Algorithm specifications

The main can be run with 3 functions/methodologies: 
<br> 
### Method 1: dominance [hexagonize_dominant]
Convert a spatial map into a map of hexagons: an overlay is made between the original map and the hexagons. In this overlay, several classes of the original map can occur within a single hexagon. The dominant class in terms of area within this hexagon (i.e. the class with the largest presence) will be assigned to the resulting hexagon map.

### Method 2: keep all & duplicate [hexagonize_keep_all]
Convert a spatial map into a map of hexagons: a spatial join is made between the original map and the hexagons. When several classes of the original map occur within a single hexagon, this will result in multiple records having the same geometry but holding different attributes from the original map.

### Method 3: keep all & duplicate [hexagonize_density]
Convert a spatial map into a map of hexagons: Convert a spatial map into a map of hexagons: a spatial overlay is made between the original map and the hexagons. When several classes of the original map occur within a single hexagon, this will result in multiple records having the same geometry but holding different attributes from the original map. Furthermore, a column density contains the proportion of the original class in a particular hexagon. For area computations, all data will be reprojected to a projected crs default 32631. The output will be delivere once again in the hexagon crs.

## Meta
@author: [Willem Boone](willem.boone@vliz.be)