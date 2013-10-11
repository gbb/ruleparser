#!/usr/bin/python

import sys
import csv
import re
import json
from collections import OrderedDict

from csv_to_array import csv_to_array

def main():

  print "Testing parse_metadata"
  print parse_md(*csv_to_array('test.csv'))

def parse_md(grid, inputs, outputs):

  # pick out variable names from row 1 and assign their values from row 2 
  # returns as a JSON string to be embedded later

  metadata=OrderedDict([])    # preserve ordering of variable names

  for i in range(0,len(grid[0])):
    var = grid[0][i]  
    val = grid[1][i]
    if var:               # if the cell contains a variable name
      var=var.upper()     # make it upper case
      re.sub('[\t\n\'"]+', '_', var)  # remove var special chars
      re.sub('[\t\n\'"]+', '_', val)  # remove val special chars
      metadata[var]=val      # assign it into hash. // embed val in double quotes 

  return "RULE_METADATA='"+json.dumps(metadata, ensure_ascii=False)+"'"
 
if __name__=='__main__':
  main()
