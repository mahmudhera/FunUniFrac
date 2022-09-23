#!/usr/bin/env python
import argparse
import os
import sys
sys.path.append('./src')
import numpy as np
from scipy import sparse
from LP_EMD_helper import get_matrix_from_edge_list




parser = argparse.ArgumentParser(description='Given an edge list file, convert it into a sparse matrix to be used'
                                             'as an input for LP_EMD.py')
parser.add_argument('-e', '--edge_list', help='Input edge list file of the KEGG hierarchy', required=True)
parser.add_argument('-o', '--out_dir', help='Output directory', required=True)

args = parser.parse_args()

edge_list = args.edge_list
out_dir = args.out_dir

basename = os.path.splitext(os.path.basename(edge_list))[0]
print(basename)