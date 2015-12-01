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


def calculate_distances(infile, ids1, ids2, q):
    """Calculate the distances between all `ids1` to `ids2` in `infile`.

    infile should be a shapefile with features, ids1 and ids2 should be
    a list of shape ids you wish to have distances calculated for.
    Distances between polygons that are both in ids1 will not be calculated
    unless they are also in ids2 and vice versa. This allows the number of
    distance queries to be limited.
    q is a multiprocessing q object to which the returned data is placed so
    that it may be accessed from the calling process.
    """
    with fiona.open(infile) as source:
        source = list(source)
        # Calculate distances and store in data
        for i, id1 in enumerate(ids1):
            i_shp = shape(source[int(i)]['geometry'])

            for j, id2 in enumerate(ids2):
                j_shp = shape(source[int(j)]['geometry'])
                if i_shp.is_valid and j_shp.is_valid:
                    dist = i_shp.distance(j_shp)
                else:
                    dist = -1

                q.put([i, j, dist])


def main():
    """Main execution thread."""
    # infile = "./data/random_points/test.shp"
    infile = "./data/low_water_final/low_water.shp"
    ids = extract_ids(infile)
    # Split ids to run distance queries on multiple processes
    c = len(ids)/2
    set1, set2 = ids[:c], ids[c:]

    # Initialize data globals
    data_1_1 = multiprocessing.Queue()
    data_2_2 = multiprocessing.Queue()
    data_1_2 = multiprocessing.Queue()

    # Initialize processes
    p = []
    p.append(multiprocessing.Process(target=calculate_distances, args=(
        infile, set1, set1, data_1_1,)))
    p.append(multiprocessing.Process(target=calculate_distances, args=(
        infile, set2, set2, data_2_2,)))
    p.append(multiprocessing.Process(target=calculate_distances, args=(
        infile, set1, set2, data_1_2,)))

    # Start all processes
    for process in p:
        process.start()

    # Initialize empty matrix for dataset
    data = [[-1 for j in ids] for i in ids]

    num_processed = 0
    total_to_process = len(set1)*len(set1) + len(set1)*len(set2) + \
        len(set2)*len(set2)
    print_progress(0, total_to_process)
    while(num_processed < total_to_process):
        if not data_1_1.empty():
            d1 = data_1_1.get()
            data[d1[0]][d1[1]] = d1[2]
            num_processed += 1
            print_progress(num_processed, total_to_process)
        if not data_1_2.empty():
            d2 = data_1_2.get()
            data[d2[0]+c][d2[1]] = d2[2]
            data[d2[1]][d2[0]+c] = d2[2]
            num_processed += 1
            print_progress(num_processed, total_to_process)
        if not data_2_2.empty():
            d3 = data_2_2.get()
            data[d3[0]+c][d3[1]+c] = d3[2]
            num_processed += 1
            print_progress(num_processed, total_to_process)

    print_progress(1, total_to_process)
    print

    # Block main execution until processes complete
    for process in p:
        process.join()

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
