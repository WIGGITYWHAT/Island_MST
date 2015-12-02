"""Create a csv matrix of distances between shapefile geometry objects.

Requirements: fiona, shapely

Written by: Taylor Denouden
Date: November 25, 2015
"""

import fiona
from shapely.geometry import shape
from multiprocessing import Pool


def extract_ids(input_file):
    """Extract all polygon ids from input shapefile."""
    with fiona.open(input_file, 'r') as source:
        return [shp['id'] for shp in source]


def calculate_distances(args):
    """Calculate distances between `shp_id` and all other features in shapefile.

    `shp_id` is the feature id in the shapefile `infile` (global). `shp_id` and
    each id in `ids` (global) are cast to shapely features and then passed to a
    distance function contained in the shapely library. An array is returned
    with all these distances.
    """
    with fiona.open(args['infile']) as source:
        source = list(source)
        result = []

        # Calculate distances and store in result
        i_shp = shape(source[int(args['shp_id'])]['geometry'])
        for j in args['ids']:
            if int(j) < int(args['shp_id']):
                result.append(-1)
                continue

            j_shp = shape(source[int(j)]['geometry'])
            if i_shp.is_valid and j_shp.is_valid:
                result.append(i_shp.distance(j_shp))
            else:
                result.append(-1)

        return result


def main():
    """Main execution thread."""
    # infile = "./data/random_points/test_polys.shp"
    infile = "./data/low_water_final/low_water.shp"
    ids = extract_ids(infile)

    # Calculate each the distance from each id to ids using a process pool
    print "Calculating distances"
    pool = Pool()
    data = pool.map(calculate_distances, [{
        'shp_id': shp_id,
        'infile': infile,
        'ids': ids,
    } for shp_id in ids], chunksize=100)

    # Write the data to a new csv file
    outfile = open("test.csv", "w")

    # Write header of output file
    print "Writing Header"
    outfile.write("NODE")
    for i in ids:
        outfile.write("," + i)
    outfile.write("\n")

    # Write rows
    print "Writing Rows"
    for i in ids:
        outfile.write(str(i) + ",")
        i = int(i)

        for j in ids:
            j = int(j)
            outfile.write(str(data[i][j]) + ",")
        outfile.write("\n")

    outfile.close()

if __name__ == "__main__":
    main()
