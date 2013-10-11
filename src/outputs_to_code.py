#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import datetime
from csv_to_array import csv_to_array
from rp_settings import debugging, data_start_row, rule_value_field, output_sql_filename

# take grid
# iterate through lines
# print sql saying 'add to the table these columns (from 'outs')
# print sql saying 'if rule=x, update values(...)' for each rule
# e.g.
# ALTER TABLE eksperiment.dddb_test_5x5_b_bare_dyrk ADD COLUMN EGNETHET char(10);
# UPDATE eksperiment.dddb_test_5x5_b_bare_dyrk SET (EGNETHET,KVALITET, HVORDAN_KJ
# ENT, KILDE) = ('Potensiell','Ukjent','Implisitt','DMK') WHERE dn=1;
# track and output which values were added so people can check no dupes by mistake. 


def debug(str):
  if debugging==1:
    print str

def main():

    print "Testing outputs_to_code"
    print outputs_to_code(*csv_to_array('test.csv'), input_filename='test.csv', layer_name='eksperiment.dbname')   # returns 3 values

def outputs_to_code(grid, inputs, outputs, input_filename, layer_name): 

    sqlstr = init_sql(input_filename, layer_name)

    sqlstr += add_index_on_value_column(layer_name)

    sqlstr += define_output_columns(outputs, layer_name) # pass in output fields

    sqlstr += assign_values_by_rule(grid, inputs, outputs, layer_name)

    return sqlstr

def init_sql(filename, layer_name):
  now = datetime.datetime.now().isoformat();
  string =  u"-- Automatically generated. To run, type:   psql (DATABASE) < add_values.sql\n"
  string += u"-- Generated on: " + now + " from the file: " + filename + "\n"
  string += u"-- This code assumes you have a geometry table: '"+layer_name+"' from gdal/rbuild.\n\n"
  return string

def add_index_on_value_column(layer_name): 
  return "create index " + layer_name + "_value_index on " + layer_name + " (value);\n"

def define_output_columns(outputs, layer_name):
  string=u""
  for c in outputs:
    string += u"alter table " + layer_name + " add column " + c[1] + " " + c[2] + ";\n"
  return string;


def assign_values_by_rule(grid, inputs, outputs, layer_name):
  # actual rules begin at line 4 (starting from 0)

  # initialise the result to be empty
  string = u''

  # extract the column names
  output_cols_indices = [val[0] for val in outputs] 
  output_cols_names = [val[1] for val in outputs] 
  columns_string = ",".join(output_cols_names)
  
  # starting from the first row of real data output values in the spreadsheet
  for row in range(data_start_row,len(grid)):

    debug("Row:"+str(row))
    debug("of"+str(len(grid)))

    if (len(grid[row])>0 and grid[row][0] != '' and not grid[row][0].startswith(u'#')):    # ignore comments
   
      debug("Is not a comment or blank row")

      # pick out items from each row at the right columns
      output_values = [grid[row][col] for col in output_cols_indices] 

      values_string = ",".join(output_values)

      debug("values are: "+values_string)

      #add the complete output colnames, values strings and row.
      #note that 'row+1' is needed to make it match the CSV row concept, used in the result raster.
      string += 'update ' + layer_name + ' set'
      string += '(' + columns_string + ') = (' + values_string + ') where ' + rule_value_field + '=' + str(row+1) + ';\n'

  return string


# emit gdalcalc script(s)

if __name__=='__main__':
  main()
