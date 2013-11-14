ruleparser
=====

Quickly and easily transform geometry datasets using a set of rules stored in a spreadsheet and raster calculations. It is designed to work with 'rbuild'.

Purpose
-----

This program translates spreadsheets into numpy algebra and SQL.

The program takes a CSV spreadsheet (e.g. from Excel or Openoffice) in a specified format as the main source of input. 
The spreadsheet describes a grid-based GIS transformation of the input rasters.

Why is this useful? Spreadsheets are easy to visualise and edit, especially for non-programmers, and relatively complex 
map transformation logic can be written and checked without needing to decipher GIS functions. By using regular grid 
cells, non-GIS users don't need to worry about things like geometry/shape/area. By using high-speed numpy functions and 
GDAL, users don't need to worry about how to optimise the code, it's almost guaranteed to run fast.

This program is used in combination with rbuild. See http://github.com/gbb/rbuild.

In our work with national maps, ruleparser and rbuild allow us to transform several national maps using a moderately 
complex set of rules at 10x10m resolution in minutes. The area covered by these maps is 1200km by 1500km.

You are welcome (and encouraged) to adapt this program to suit your own needs. Some hints for alternative grammars are 
provided in the source code.

There are some settings in rp_settings.py that you can adjust.

Input Format
-----

The input is a CSV spreadsheet in the following format (see test.csv).

1st line of spreadsheet: metadata variable names for this spreadsheet/transform

2nd line of spreadsheet: metadata values describing this spreadsheet/transform

3rd line: empty

4th line: each column will be either an input, an output, or a comment field.
By default all columns are comment fields and are ignored, unless marked by in/ or out/

- Input fields have the format:   in/NAME/input_raster_filename

- Output fields have the format:  out/NAME/postgres_datatype

5th line onwards:
Input and output values according to the column format specified in the 4th line, as follows:

Input values: 

  Simple numbers 1 2 3 99     (integers; adjust source code if you want reals)

  Closed ranges  3...10, 1...100

  Lists:   1, 2, 3...10, 1...100      simple numbers and closed ranges


- Empty rows are ignored.
- Rows beginning with # are ignored.
- In row 4, columns that don't contain 'in/x/y' or 'out/x/y' are ignored. 

Output values: 
  
- Whichever values are to be produced for the SQL database.

Program outputs
---

The program will generate two files (and dump to screen). 

- "new_calc.py"  has code that carries out a high-speed numpy calculation

- "add_values.sql" has code to update a polygonized raster. 

How to run
-------

First make sure you have installed the following e.g. with yum:

- pip   (python-pip)
- libxml, libxml2 and libxml2-devel
- libxslt and libxslt-devel
- lxml extension to python:  (pip install lxml)
- pyparsing extension to python (easy_install pyparsing)

How to run the code with an example file: 

> ./ruleparser.py test.csv my_postgres_table

Author and license
-----

Hope you find this useful!

Graeme Bell, Skog og Landskap
grb@skogoglandskap.no

License: GPL v3.
Thanks to the Norwegian Forest & Landscape Institute for open sourcing this work.


Notes
-----

1. If you are having trouble getting your spreadsheet to parse, enable debugging
in rp_settings.py, and see which cell is causing the problem. It's common to
accidentally use e.g. 1..3 instead of 1...3. (1..3 can be parsed as a date 
in openoffice). 


2. This program uses the pyparsing module - take a look at src/inputs_to_code.py.
It's pretty useful.

