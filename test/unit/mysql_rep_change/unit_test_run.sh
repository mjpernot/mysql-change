#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
test/unit/mysql_rep_change/create_instances.py
test/unit/mysql_rep_change/crt_slv_mst.py
test/unit/mysql_rep_change/help_message.py
test/unit/mysql_rep_change/is_slv_up.py
test/unit/mysql_rep_change/main.py
test/unit/mysql_rep_change/move_slave.py
test/unit/mysql_rep_change/move_slave_up.py
test/unit/mysql_rep_change/mv_slv_to_new_mst.py
test/unit/mysql_rep_change/run_program.py
