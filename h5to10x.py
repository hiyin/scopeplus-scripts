#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scipy import sparse
import scipy.io as sio
import h5py
import os
import argparse

parser = argparse.ArgumentParser(description = 'Convert the h5 file to the 10x mtx')
parser.add_argument('-i', '--input', required=True, help='Input h5')
parser.add_argument('-o', '--output', required=True, help='output path matrix.mtx gene.tsv barcode.tsv file')
parser.add_argument('-d', '--dataset', required=True, help='Input datasetname')

args = parser.parse_args()
filename = args.input
path = args.output
dataset = args.dataset

if(os.path.exists(path)==False):
	os.mkdir(path)

with h5py.File(filename, "r") as f:
    slotname = "/."+dataset+"_dimnames/"
    barcode = np.array(f[slotname+"2"])
    genes = np.array(f[slotname+"1"])
    matrix = np.array(f[dataset]).T

sA = sparse.csr_matrix(matrix) 
sio.mmwrite(path+"/matrix.mtx",sA)

df_gene = pd.DataFrame(genes)
df_gene[0] = df_gene[0].str.decode("utf-8")
df_gene.to_csv(path+"/genes.tsv",header=False,index=False,sep='\t')

df_barcode = pd.DataFrame(barcode)
df_barcode[0] = df_barcode[0].str.decode("utf-8")
df_barcode.to_csv(path+"/barcodes.tsv",header=False,index=False,sep='\t')