#!/usr/bin/env python
# coding: utf-8
import csv
import os
import argparse
import logging

parser = argparse.ArgumentParser(description = 'Convert the mtx file to the MongoDB csv')
parser.add_argument('-o', '--output', required=True, help='Output path of the csv file')
parser.add_argument('-m', '--matrix', required=True, help='Input matrix.mtx file')
parser.add_argument('-g', '--genes', required=True, help='Input gene.tsv file')
parser.add_argument('-b', '--barcodes', required=True, help='Input barcodes.tsv file')
parser.add_argument('-c', '--cohort', default="", help='Cohort identifier to append to barcode name, default: None')
parser.add_argument('-f', '--feature', required=True, help='Input barcodes.tsv file')

args = parser.parse_args()

barcodes = os.path.abspath(args.barcodes)
genes = os.path.abspath(args.genes)
mtx = os.path.abspath(args.matrix)
result = os.path.abspath(args.output)
cohort_id = args.cohort

def convert_mtx(barcodes,genes ,mtx,result = "result.csv",cohort_id = ""):
    # Read the barcode file

    print("Barcodes file"+barcodes)
    print("Genes file"+genes)
    print("MTX file"+mtx)
    print("Result file"+result)

    with open(barcodes, newline='') as f1:
        reader1 = csv.reader(f1)
        barcodes = list(reader1)
    # Read the gene file
    with open(genes, newline='') as f2:
        reader2 = csv.reader(f2)
        genes = list(reader2)


    try:
        # open file in read mode and writ file in the write mode
        with open(mtx, 'r') as read_obj, open(result,'w') as write_obj:
                # Construct writers
                count = 0
                csv_reader = csv.reader(read_obj)
                csv_writer = csv.writer(write_obj)
                next(csv_reader, None)  # skip the headers
                next(csv_reader, None)  # skip the headers

                # Iterate over each row in the csv using reader object
                for row in csv_reader:
                    # row variable is a list that represents a row in csv
                    r = (row[0].split(" "))

                    try:
                        r[0] = str(genes[int(r[0])-1][0])
                    except IndexError:
                        pass
                    
                    try:
                        r[1] = str(barcodes[int(r[1])-1][0])+str(cohort_id)
                    except IndexError:
                        pass
                    
                    csv_writer.writerow(r)
                    count=count+1

                    if(count%10000==0):
                        print(str(count)+" rows are processed")
    except Exception as e:
        logging.error(e)
        logging.error("Cannot parse:")


convert_mtx(barcodes,genes ,mtx,cohort_id=cohort_id,result = result)

