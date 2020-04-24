#!/bin/bash
# Unit test code coverage for program module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#   that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_rep_change test/unit/mysql_rep_change/crt_slv_mst.py
coverage run -a --source=mysql_rep_change test/unit/mysql_rep_change/fetch_slv.py
coverage run -a --source=mysql_rep_change test/unit/mysql_rep_change/help_message.py
coverage run -a --source=mysql_rep_change test/unit/mysql_rep_change/is_slv_up.py
coverage run -a --source=mysql_rep_change test/unit/mysql_rep_change/move_slave.py
coverage run -a --source=mysql_rep_change test/unit/mysql_rep_change/mv_slv_to_new_mst.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
