"""
This script demonstrates the usage of hexagonizing function to convert a
polygon map into hexagons. Additionally, the hexagons can be converted into
center points.
"""

__author__ = "Willem Boone"
__email__ = "willem.boone@vliz.be"

import geopandas as gpd
import os
from hexagonize import hexagonize_dominant
from hexagonize import hexagonize_keep_all
from hexagonize import hexagonize_density
from hexagonize import to_centroids
from pathlib import Path

# -----------------------------------------------------------------------------
# SETTINGS
# -----------------------------------------------------------------------------
# add the path to following files:
# - map: the map you want to convert
# - hexagons: shapefile containing hexagons you need to convert the map to.
# - processing: a directory where to store results
# Notice: make sure the map and hexagon file have the same projection.

# path to source map
map = "EUSeaMap_2023.gdb"

# shapefile containing the hexagons
hexagons = "hexagon_grid/hexagon_grid.shp"

# path to write preprocessed data
out_path = "output_map_conversion"

# post process
map_name = Path(map).stem
if not os.path.exists(out_path):
    os.makedirs(out_path)

# -----------------------------------------------------------------------------
# READ DATA
# -----------------------------------------------------------------------------
print("reading data")
hexagon_gdf = gpd.read_file(hexagons)
map_gdf = gpd.read_file(map, mask=hexagon_gdf)
map_gdf.to_file(os.path.join(out_path, f"clip_{map_name}.shp"))

# -----------------------------------------------------------------------------
# PROCESSING
# -----------------------------------------------------------------------------
# Define hexagonize function and convert to points.
print("processing data")
map_processed = hexagonize_density(map_gdf=map_gdf, hexagon_gdf=hexagon_gdf)
map_processed = to_centroids(map_processed)

# -----------------------------------------------------------------------------
# POSTPROCESSING
# -----------------------------------------------------------------------------
# add the additional required columns
map_processed["EventDate"] = ""
map_processed["FieldNumber"] = ""
map_processed["ScientificName"] = map_name

# save results
dest = os.path.join(out_path, f"{map_name}_hexagon_centroids.csv")
map_processed.to_csv(dest)
dest = os.path.join(out_path, f"{map_name}_hexagon_centroids.shp")
map_processed.to_file(dest)
print("finished")
