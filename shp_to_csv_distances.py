#!/usr/bin/env python
"""Create a csv matrix of distances between shapefile geometry objects.

Requirements: fiona, shapely

Written by: Taylor Denouden
Date: November 25, 2015
"""

from __future__ import print_function
import sys
import fiona
from shapely.geometry import shape
from multiprocessing import Pool, cpu_count


def extract_ids(input_file):
    """Extract all polygon ids from input shapefile."""
    with fiona.open(input_file, 'r') as source:
        return [shp['id'] for shp in source]


def calc_dists(args):
    """Calculate distances between `shp_id` and all other features in shapefile.

    `shp_id` is the feature id in the shapefile `infile` (global). `shp_id` and
    each id in `ids` (global) are cast to shapely features and then passed to a
    distance function contained in the shapely library. An array is returned
    with all these distances.
    """
    i = args[0][0]
    i_shp = args[0][1]
    shps = args[1]
    result = []

    # Calculate distances and store in result
    for (j, j_shp) in shps:
        if int(j) < int(i):
            dist = -1
        else:
            try:
                dist = i_shp.distance(j_shp)
            except Exception as e:
                with open(sys.path.join("logs", i, ".txt", "w+")) as logfile:
                    logfile.write(e + "\n")
                dist = -2

        result.append(dist)

    return result


def main():
    """Main execution thread."""
    # infile = "./data/random_points/test_polys.shp"
    infile = "./data/low_water_final/low_water.shp"
    ids = extract_ids(infile)
    shapes = []

    # Get all shapefiles in memory as shapely shapes
    with fiona.open(infile) as source:
        source = list(source)
        shapes = [(i, shape(source[int(i)]['geometry'])) for i in ids]

    # Calculate each the distance from each id to ids using a process pool
    print("Calculating distances")
    pool = Pool(processes=cpu_count(), maxtasksperchild=5)
    data = pool.map(calc_dists, [(i, shapes) for i in shapes], chunksize=50)

    # Write the data to a new csv file
    with open("test.csv", "w") as outfile:

        # Write header of output file
        print("Writing Header")
        outfile.write("NODE,")
        outfile.write(",".join(ids))
        outfile.write("\n")

        # Write rows
        print("Writing Rows")
        for i in ids:
            outfile.write(i + ",")
            outfile.write(",".join([str(j) for j in data[int(i)]]))
            outfile.write("\n")

if __name__ == "__main__":
    main()
