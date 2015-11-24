"""Command line argument parser and help text for djikstra algorithm script.

Written by: Taylor Denouden
Date: November 24, 2015
"""
__all__ = ['args']  # export only args variable
import argparse


parser = argparse.ArgumentParser(description="""Calculate the minimum
                                 spanning tree of a distance matrix.""")
parser.add_argument('matrix', help='the input csv distance matrix')
parser.add_argument('start_node',
                    help='column name of starting node in the mst algorithm')
parser.add_argument('-p', '--print', dest="print_out", action="store_true",
                    help='flag to print output to stdout')
parser.add_argument('-o', metavar="out.csv", dest="outfile", default="out.csv",
                    help='the default output csv file')

args = parser.parse_args()
