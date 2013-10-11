#!/usr/bin/python

from pyparsing import *
from lxml import etree
import csv
import string
from csv_to_array import csv_to_array
from rp_settings import debugging, data_start_row, error_code


## pyparsing will be used to parse cell contents
## csv will be used to parse csv into cells

## Define the grammar to be used by thepyparsing module - BNF style description.

# A simple number can be used to match a contiguous set of digits.
simplenumber = Word(nums).setResultsName("sn") 

# An asterisk can be used to say 'match any value for this field'. 
wildcard = Literal("any").setResultsName("wildcard") | Literal("*").setResultsName("wildcard")

# A closed range matches all the numbers including and between two numbers separated by '...'
closedrange = Group(Word(nums).setResultsName("low") + Literal("...").suppress() + Word(nums).setResultsName("high")).setResultsName("closedrange")

# An expression is either a closed range, a wildcard, or a simple number. 
expression = Group(closedrange | simplenumber | wildcard).setResultsName("expression");

# An expression list is a series of one or more expressions seperated by ','. Whitespaces are allowed. 
# Notice that ',' is correctly picked up from a csv file because of escape characters. 
# In practice, an expressionlist will match if any element of the list matches.
expressionlist = delimitedList(expression, delim=',').setResultsName("list");

# A valid cell is an expressionlist followed by nothing more.
cell = expressionlist + StringEnd()

# NOTE: don't use ^ in the 'expression' statement above.
# It matches the longest string (greedy matching). This creates problems with closedranges

def debug(str):
  if debugging==1:
    print str

def main():
  
  print "Testing inputs_to_code"
  print
  print inputs_to_code(*csv_to_array('test.csv'))   # csv_to_array returns 3 values
  print


def descend(root,currentLetter):

  # match single numbers with numpy equality operator
  if root.tag == "sn":
    return(currentLetter + "==" + root.text)

  # match wildcard by doing no comparison at all 
  elif root.tag == "wildcard":
    return("") # empty string , e.g. no calculation.

  # match closedrange with a pair of <= and >= in numpy, multiplied together
  elif root.tag == "closedrange":
    return("fa.all([" + currentLetter + ">=" + root.find("low").text + "," + 
      currentLetter + "<=" + root.find("high").text + "])" )  # UPDATED

  elif root.tag == "expression":
    output=""
    if root[0].tag == "wildcard":        #optimise out 'wildcards' from the expression e.g. remove () which will break multiplication.
      return ("")		    #
    else:
      for child in root:
        output+=descend(child,currentLetter)
      return (output)       # todo: is this still needed with a non-mathematical implementation?
#      return ("("+output+")")       # todo: is this still needed with a non-mathematical implementation?


  elif root.tag == "list":
    if len(root)==1:
      return(descend(root[0],currentLetter))  # if one item, don't wrap in an "OR" statement.
    else:
      outputstrings=[]      # UPDATED be sure to use fa.any, not np.any, which is 15* slower

      for child in root:                     
        outputstrings.append(descend(child,currentLetter))

      return ("fa.any(["+(",".join(outputstrings))+"])")   # items seperated by , wrapped in any

  else:
    raise Exception("Broken spreadsheet - could not process input: "+root.tag)
    sys.exit()


def inputs_to_code(grid, inputs, outputs):
    
  rules=[]
  rule_outputs=[]

  # starting from the first row with rules

  for i in range(data_start_row, len(grid)):
    row=grid[i]
    processed_input_cells=[]
    debug('  ---   '.join(row))
    if (len(row)>0 and row[0] != '' and not (row[0].startswith(u'#'))):   # ignore blank/comment lines
      debug("Parsing rule in CSV row: "+str(i+1)+" as raster output value "+str(i+1))
      rule_outputs.append(str(i+1))
      
      for n in range(0, len(inputs)):

        input_col_number=inputs[n][0]
        input_col_name=inputs[n][1]
        input_raster_name=inputs[n][2]
        debug("Parsing input column "+input_raster_name);
        
        current_cell=descend(etree.fromstring(cell.parseString(row[input_col_number]).asXML()),input_raster_name);
        processed_input_cells.append(current_cell)

      debug(processed_input_cells);

      # Remove empty strings
      # Should program terminate on finding an empty input cell, since no valid input specified?
      # or generate rule that will never match? 
 
      without_empties=filter(None,processed_input_cells)  # this removes empty strings from the array.
      if len(without_empties)==0:
        tempstring='(A==A)'    # array of 'True' of appropriate numpy shape for a rule of form *, *, * ... 
      else:
        tempstring='fa.all(['
        tempstring+=','.join(without_empties)  
        tempstring+='])'
      rules.append(tempstring)

      debug("Appending " + str(tempstring))

  # now print out numpy code fragments within a giant select statement, in order.
  # assuming 'most general' rules are at the top and 'most specific' are at the bottom
  # it's necessary to reverse the order of the lists.

  rules.reverse()
  rule_outputs.reverse()

  # NODATA should be handled in the transform spreadsheet directly.

  # print out rules and outputs in python select() format, as a BASH variable
  # no newlines or gdal_calc will crash

  outputstring="RULE_FORMULA='ss.select(["
  outputstring+=",".join(rules)
  outputstring+="],["
  outputstring+=",".join(rule_outputs)
  outputstring+="],"+error_code+")'"

  return outputstring



if __name__=='__main__':
  main()
