# Should we print debug information? 0=no, 1=yes
# Enable this if your spreadsheet isn't parsing, to find the bug.

debugging = 0

# This constant represents the boundary between the metadata and data parts of the CSV

data_start_row = 4

# What 'rule number' should be output if no rules match?
# This can be used to check that a rule set is covering all possible input combinations.

error_code='199'

# What is the name of the value field that gdal_polygonize/gdal_trace_outline will create?

rule_value_field = 'value'          # may be 'dn' for gdal_polygonize

# Where should the output SQL be stored?

output_sql_filename = 'add_values.sql'

# Where should the numpy calculation be stored?

output_calc_filename = 'calc_new.sh'
