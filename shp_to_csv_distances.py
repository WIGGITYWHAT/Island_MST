"""Create a csv matrix of distances between shapefile geometry objects.

Requirements: fiona, shapely

Written by: Taylor Denouden
Date: November 25, 2015
"""

import random
import fiona
from shapely.geometry import shape
from scripts.printer import print_progress


def main():
    """Main script execution."""
    outfile = open("out.csv", "w")
    ids = extract_ids("data/high_polys.shp")

    # Write header
    print "Writing Header"
    outfile.write("NODE")
    for i in ids:
        outfile.write("," + i)
    outfile.write("\n")

    # Write rows
    print "Writing Rows"
    for i, j in enumerate(ids):
        print_progress(i/len(ids))
        outfile.write(j)
        write_row_distances(j, ids, "data/high_polys.shp", outfile)
        outfile.write("\n")
    print_progress(1)
    print


def extract_ids(input_file):
    """Extract all polygon ids from input shapefile."""
    with fiona.open(input_file, 'r') as source:
        return [shp['id'] for shp in source]


def write_row_distances(i, ids, input_file, outfile):
    """Write distances between shape with id i and all other shapes in ids."""
    with fiona.open(input_file, 'r') as source:
        source = list(source)
        i_shp = shape(source[int(i)]['geometry'])

        for j in ids:
            j_shp = shape(source[int(j)]['geometry'])
            if i_shp.is_valid and j_shp.is_valid:
                dist = i_shp.distance(j_shp)
            else:
                dist = -1

            outfile.write("," + str(dist))

if __name__ == "__main__":
    main()
