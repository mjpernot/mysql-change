#!/usr/bin/python
# Classification (U)

"""Program:  crt_slv_mst.py

    Description:  Unit testing of crt_slv_mst in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/crt_slv_mst.py

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
        self.read_only = "OFF"
        self.server_id = 10
        self.sql_user = "User"
        self.sql_pass = None
        self.machine = "Linux"
        self.host = "HostName"
        self.port = 3306
        self.defaults_file = None


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_found_slave -> Test with no slave found.
        test_readonly_slave -> Test with readonly slave found.
        test_found_slave -> Test with slave found.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()
        self.slaves = [self.slave]
        self.new_mst = "SlaveName"
        self.master = "MasterName"
        self.result_msg = \
            "Error:  New master SlaveName is set to read-only mode."
        self.result_msg2 = \
            "Error: Slave(new master) SlaveName was not found in slave array."

    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_no_found_slave(self, mock_find):

        """Function:  test_no_found_slave

        Description:  Test with no slave found.

        Arguments:

        """

        mock_find.return_value = None

        master, err_flag, err_msg = mysql_rep_change.crt_slv_mst(
            self.slaves, new_mst=self.new_mst)

        self.assertEqual((master, err_flag, err_msg),
                         (None, True, self.result_msg2))

    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_readonly_slave(self, mock_find):

        """Function:  test_readonly_slave

        Description:  Test with readonly slave found.

        Arguments:

        """

        self.slave.read_only = "ON"
        mock_find.return_value = self.slave

        master, err_flag, err_msg = mysql_rep_change.crt_slv_mst(
            self.slaves, new_mst=self.new_mst)

        self.assertEqual((master, err_flag, err_msg),
                         (None, True, self.result_msg))

    @mock.patch("mysql_rep_change.mysql_class.MasterRep",
                mock.Mock(return_value="MasterName"))
    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_found_slave(self, mock_find):

        """Function:  test_found_slave

        Description:  Test with slave found.

        Arguments:

        """

        mock_find.return_value = self.slave

        master, err_flag, err_msg = mysql_rep_change.crt_slv_mst(
            self.slaves, new_mst=self.new_mst)

        self.assertEqual((master, err_flag, err_msg),
                         (self.master, False, None))


if __name__ == "__main__":
    unittest.main()
