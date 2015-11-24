#!/usr/bin/python
"""Main Djikstra's Algorithm implementation.

Create nodes from input file and exports the minimum distance between the
specified starting node and every other node.

For help run `python main.py --help`

Written by: Taylor Denouden
Date: November 24, 2015
"""

import csv
from scripts.node import Node
from scripts.args import args


def main():
    """Main script execution."""
    # Read in data and build graph data structure
    nodes = build_graph(args.matrix)

    # Calculate minimum spanning tree with Djikstra's algorithm
    distances, previous = calculate_mst(nodes, args.start_node)

    # Print result
    if args.print_out:
        print "Start node:", args.start_node, "\n"
        print_table(distances, previous)

    # Write result to css
    write_output(args.outfile, distances, previous)


def build_graph(input_file):
    """Build the graph data structure from the input csv file."""
    # Open the csv as dict iterator
    input_file = open(input_file, 'rU')
    reader = csv.DictReader(input_file)

    # Create all nodes
    nodes = {}
    for row in reader:
        name = row['NODE']
        nodes[name] = Node(name)

    # Return to start of file
    input_file.seek(0)
    # Skip header row
    reader.next()

    # Set neighbors if distance >= 0
    for row in reader:
        name = row['NODE']
        node = nodes[name]

        neighbors = [nodes[i] for i in row.keys()
                     if i != "NODE" and float(row[i]) >= 0]

        for neighbor in neighbors:
            if neighbor != node:
                node.set_neighbor(neighbor, float(row[neighbor.name]))

    return nodes


def calculate_mst(nodes, start_node):
    """Calculate minimum spanning tree with Djikstra's algorithm.

    Inputs: nodes
    Outputs: distances [dict] of distances between start node and all others
             previous [dict] of previous node visited before node
    """
    distances = {}
    previous = {}

    # Assign tentative distance values
    for key in nodes.keys():
        distances[key] = float('Inf')
    distances[start_node] = 0

    # Set current and create unvisited set
    current = nodes[start_node]

    while(current):
        # Look at all neighbors and compare distances
        for neighbor in current.get_unvisited_neighbors():
            alt = distances[current.name]+current.get_distance(neighbor)
            if alt < distances[neighbor.name]:
                distances[neighbor.name] = alt
                previous[neighbor.name] = current.name

        # Mark current node as visited
        current.set_visited(True)
        # iterate current to closest neighbor
        current = current.get_closest_unvisited_neighbor()

    return distances, previous


def write_output(outfile, distances, previous):
    """Write results to output csv file."""
    with open(outfile, "w") as outfile:
        fieldnames = ['node', 'dist', 'prev']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for key in distances.keys():
            writer.writerow({
                'node': key,
                'dist': distances[key],
                'prev': previous.get(key, "-")
            })


def print_table(distances, previous):
    """Print out node distances and order in a nice tabular format."""
    print "{:^10} | {:^10} | {:^10}".format("Node", "Distance", "Previous")
    print "-"*36
    for (k, v) in distances.iteritems():
        print "{:^10} | {:>10} | {:^10}".format(k, v, previous.get(k, "-"))


if __name__ == "__main__":
    main()
