#!/usr/bin/python
# Classification (U)

"""Program:  fetch_slv.py

    Description:  Unit testing of fetch_slv in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/fetch_slv.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import mysql_rep_change
import version

__version__ = version.__version__


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Server_Name"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_found_slave -> Test with no slave found.
        test_found_slave -> Test with slave found.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()
        self.slaves = [self.slave]
        self.slv_mv = "SlaveName"
        self.msg = "Error:  Slave SlaveName was not found in slave array."

    #@unittest.skip("Bug: slv is not initialized anywhere in function")
    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_no_found_slave(self, mock_find):

        """Function:  test_no_found_slave

        Description:  Test with no slave found.

        Arguments:

        """

        mock_find.return_value = None

        slave, err_flag, err_msg = mysql_rep_change.fetch_slv(
            self.slaves, slv_mv=self.slv_mv)

        self.assertEqual((err_flag, err_msg), (True, self.msg))

    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_found_slave(self, mock_find):

        """Function:  test_found_slave

        Description:  Test with slave found.

        Arguments:

        """

        mock_find.return_value = self.slave

        slave, err_flag, err_msg = mysql_rep_change.fetch_slv(
            self.slaves, slv_mv=self.slv_mv)

        self.assertEqual((err_flag, err_msg), (False, None))


if __name__ == "__main__":
    unittest.main()
