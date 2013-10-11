#!/usr/bin/python

import sys
import os.path
sys.dont_write_bytecode=True
sys.path.append('./src')
from csv_to_array import csv_to_array, print_grid
from metadata import parse_md
from inputs_to_code import inputs_to_code
from outputs_to_code import outputs_to_code
from rp_settings import output_sql_filename, output_calc_filename


if (len(sys.argv) < 3):
  print
  print "Ruleparser: please provide a CSV spreadsheet and database name."
  print "For information about the format, please see README.md"
  print "./ruleparser.py  input.csv  my_postgres_table"
  print
  sys.exit()

spreadsheet = sys.argv[1]
layer = sys.argv[2]

if not os.path.isfile(spreadsheet):
  print
  print "Error. The spreadsheet file does not exist: "+spreadsheet
  print
  sys.exit()

print "\nParsing spreadsheet: ", spreadsheet, "\n"

# 0. Load csv to grid
grid_tuple=csv_to_array(spreadsheet)

# 1. parse grid for metadata (top 3 lines)
metadata_bash_string=parse_md(*grid_tuple)

# 2. parse grid for inputs. ( filter for in_, generate to row number and raster calc)
formula_string=inputs_to_code(*grid_tuple)

# put metadata and formula into 'input' rule formula file. 

print "------------   CUT HERE:  "+output_calc_filename+"    ----------------\n"
print metadata_bash_string, "\n"
print formula_string, "\n\n"

# 3. parse grid for outputs. 
# write a second option for raster outputs later. for now, geom. 
# filter for out_ columns. then simply substitute all values in the row, with quoting
# finally output a list of output values found so user can check. 

sql_transform=outputs_to_code(*grid_tuple, input_filename=spreadsheet, layer_name=layer)

print "------------   CUT HERE:  "+output_sql_filename+"    ----------------\n"
print sql_transform, "\n\n"

