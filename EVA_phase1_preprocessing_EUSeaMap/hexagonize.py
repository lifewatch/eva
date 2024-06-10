import geopandas as gpd
from shapely.geometry import Point

__author__ = "Willem Boone"
__email__ = "willem.boone@vliz.be"


def hexagonize_dominant(map_gdf: gpd.GeoDataFrame,
                        hexagon_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Convert a spatial map into a map of hexagons: an overlay is made between
    the original map and the hexagons. In this overlay, several classes of the
    original map can occur within a single hexagon. The dominant class in terms
     of area within this hexagon (i.e. the class with the largest presence)
     will be assigned to the resulting hexagon map.
    :param map_gdf: geopandas dataframe containing the original map/
    :param hexagon_gdf: geopandas dataframe containing the hexagons.
    :return: geopandas dataframe of the hexaginized map.
    """
    # spatial overlay: creates polygons by merging boundaries of both gdf
    overlay = gpd.overlay(hexagon_gdf, map_gdf)

    # sort all polygons on area to havethe dominant/largest one first
    overlay["area"] = overlay.area
    overlay = overlay.sort_values('area', ascending=False)

    # dissolve based on FID, parameters of dominant polygon are kept
    overlay = overlay.dissolve(by='FID', aggfunc='first')

    return overlay


def hexagonize_keep_all(map_gdf: gpd.GeoDataFrame,
                        hexagon_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Convert a spatial map into a map of hexagons: a spatial join is made
    between the original map and the hexagons. When several classes of the
    original map occur within a single hexagon, this will result in multiple
    records having the same geometry but holding different attributes from the
    original map.
    :param map_gdf: geopandas dataframe containing the original map/
    :param hexagon_gdf: geopandas dataframe containing the hexagons.
    :return: geopandas dataframe of the hexaginized map.
    """
    joined = gpd.sjoin(left_df=hexagon_gdf, right_df=map_gdf, how='left')
    return joined


def hexagonize_density(map_gdf: gpd.GeoDataFrame,
                       hexagon_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Convert a spatial map into a map of hexagons: a spatial overlay is made
    between the original map and the hexagons. When several classes of the
    original map occur within a single hexagon, this will result in multiple
    records having the same geometry but holding different attributes from the
    original map. Furthermore, a column density contains the proportion of the
    original class in a particular hexagon. For area computations, all data
    will be reprojected to a projected crs default 32631. The output will be
    delivere once again in the hexagon crs.
    :param map_gdf: geopandas dataframe containing the original map/
    :param hexagon_gdf: geopandas dataframe containing the hexagons.
    :param crs: int, EPSG number for output crs.
    :return: geopandas dataframe of the hexaginized map.
    """
    # save the original crs
    hexagon_crs = hexagon_gdf.crs

    # calculate area of each hexagon
    hexagon_gdf["hexagon_area"] = hexagon_gdf.area
    # save geometry as field
    hexagon_gdf["hexagon_geo"] = hexagon_gdf.geometry

    # spatial overlay: creates polygons by merging boundaries of both gdf
    overlay = gpd.overlay(hexagon_gdf, map_gdf)

    # get area of overlay polygons
    overlay["v_map_area"] = overlay.area

    # get density
    overlay["Density"] = overlay["v_map_area"] / overlay["hexagon_area"]

    # drop confusing cols
    overlay = overlay.drop(columns=["v_map_area"])

    # reset original geometry
    overlay = overlay.drop(columns=["geometry"])
    overlay = overlay.rename(columns={'hexagon_geo': 'geometry'})
    overlay = overlay.set_geometry("geometry")
    overlay = overlay.to_crs(hexagon_crs)

    return overlay


def to_centroids(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Convert the polygon geometry of a GeoDataFrame to centroids.
    :param gdf: (GeoDataFrame) Input GeoDataFrame with polygon geometry.
    :param geometry: (str) Name of the column containing polygon geometry.
    Default is "hexagon_geo".
    :return: (GeoDataFrame) GeoDataFrame with centroids geometry.
    """
    gdf['geometry'] = gdf.geometry.centroid
    gdf['geometry'] = gdf['geometry'].apply(lambda x: Point(x))

    gdf['Lon'] = gdf["geometry"].x
    gdf['Lat'] = gdf["geometry"].y

    # gdf = gdf.drop(columns=["geometry"])

    return gdf
