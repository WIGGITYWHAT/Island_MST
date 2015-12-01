"""Create a csv matrix of distances between shapefile geometry objects.

Requirements: fiona, shapely

Written by: Taylor Denouden
Date: November 25, 2015
"""

import fiona
from shapely.geometry import shape
import multiprocessing
from scripts.printer import print_progress


def extract_ids(input_file):
    """Extract all polygon ids from input shapefile."""
    with fiona.open(input_file, 'r') as source:
        return [shp['id'] for shp in source]


def calculate_distances(args):
    """Calculate the distances between all `ids1` to `ids2` in `infile`.

    infile should be a shapefile with features, ids1 and ids2 should be
    a list of shape ids you wish to have distances calculated for.
    Distances between polygons that are both in ids1 will not be calculated
    unless they are also in ids2 and vice versa. This allows the number of
    distance queries to be limited.
    q is a multiprocessing q object to which the returned data is placed so
    that it may be accessed from the calling process.
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

            # Update progress bar
            lock.acquire()
            processed.value += 1
            print_progress(processed.value, len(args['ids'])*len(args['ids']))
            lock.release()

        return result


def main():
    """Main execution thread."""
    # infile = "./data/random_points/test.shp"
    infile = "./data/low_water_final/low_water.shp"
    ids = extract_ids(infile)

    # Calculate each the distance from each id to ids using a process pool
    pool = multiprocessing.Pool()
    data = pool.map_async(calculate_distances, [{
        'shp_id': shp_id,
        'infile': infile,
        'ids': ids,
    } for shp_id in ids])

    # Get the result of the async_map call when it is ready
    data = data.get()

    # print %100 progress
    print_progress(len(ids)*len(ids), len(ids)*len(ids))
    print

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
    lock = multiprocessing.Lock()
    processed = multiprocessing.Value('i', 0)
    main()
