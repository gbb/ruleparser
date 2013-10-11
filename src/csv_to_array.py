#!/usr/bin/python

import sys
sys.path.append('../')
import sys
import csv
import codecs
from rp_settings import debugging

def main():

  print "Testing parse_metadata"

  grid,ins,outs = csv_to_array('test.csv')

  print_grid(grid)
  print_ins_outs(ins,outs)


def print_grid(grid):
  for row in grid:
    print ", ".join(row);


def print_ins_outs(ins,outs):
   for i in ins:
     print "Input field found: name =",i[1],", column =",i[0]
   for i in outs:
     print "Output field found: name =",i[1],", column =",i[0]
  

def csv_to_array(filename):

  # settings

  dialect=csv.excel
  encoding="utf-8" 

  # initialise output arrays

  grid=[]   #  a 2D array of cells from the csv file
  ins=[]	  #  a list of index,name pairs of the input columns
  outs=[]	  #  a list of index,name pairs of the output columns

  # main

  with open(filename, 'rb') as csvfile:

    reader = csv.reader(csvfile, dialect)

    for row in reader:
      grid.append([unicode(cell, encoding) for cell in row])

    # rows 0-2 are metadata
    # row 3 is column names

    for i in range (len(grid[3])): 
      name = grid[3][i]

      if name.startswith("in/"):
        name_parts = name.split("/")
        fieldname=name_parts[1]
        rastername=name_parts[2]
        ins.append((i,fieldname,rastername))

      if name.startswith("out/"):
        name_parts = name.split("/")
        fieldname=name_parts[1]
        fieldtype=name_parts[2]
        outs.append((i,fieldname,fieldtype))
 
    return (grid, ins, outs);





if __name__=='__main__':
  main()
