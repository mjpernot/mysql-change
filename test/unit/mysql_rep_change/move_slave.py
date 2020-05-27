#!/usr/bin/python
# Classification (U)

"""Program:  move_slave.py

    Description:  Unit testing of move_slave in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/move_slave.py

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
import mysql_rep_change
import version

__version__ = version.__version__


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__ -> Class initialization.
        upd_mst_status -> upd_mst_status method.

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

    def upd_mst_status(self):

        """Method:  upd_mst_status

        Description:  upd_mst_status method.

        Arguments:

        """

        return True


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
        test_no_r_option -> Test with no -R option selected.
        test_r_option -> Test with -R option selected.
        test_move_fails -> Test with move of slave to master fails.
        test_create_slave_fails -> Test with create of slave fails.
        test_fetch_slv_fails -> Test with fetching slave fails.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()
        self.slaves = [self.slave]
        self.err_msg = "Error: Fetch Failed"
        self.err_msg2 = "Error: Create Slave Failed"
        self.err_msg3 = "Error: Move of Slave to Master Failed"
        self.args = {"-R": True}
        self.args2 = {}
        self.new_mst = "NewMaster"

    @mock.patch("mysql_rep_change.is_slv_up", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.crt_slv_mst",
                mock.Mock(return_value=("NewMaster", False, None)))
    @mock.patch("mysql_rep_change.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mv_slv_to_new_mst",
                mock.Mock(return_value=(False, None)))
    def test_no_r_option(self):

        """Function:  test_no_r_option

        Description:  Test with no -R option selected.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_change.move_slave(
                self.master, self.slaves, args=self.args2,
                new_mst=self.new_mst), (False, None))

    @mock.patch("mysql_rep_change.mysql_libs.reset_slave",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.chg_slv_state",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.find_name",
                mock.Mock(return_value="SlaveMaster"))
    @mock.patch("mysql_rep_change.is_slv_up", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.crt_slv_mst",
                mock.Mock(return_value=("NewMaster", False, None)))
    @mock.patch("mysql_rep_change.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mv_slv_to_new_mst",
                mock.Mock(return_value=(False, None)))
    def test_r_option(self):

        """Function:  test_r_option

        Description:  Test with -R option selected.

        Arguments:

        """

        self.assertEqual(
            mysql_rep_change.move_slave(
                self.master, self.slaves, args=self.args,
                new_mst=self.new_mst), (False, None))

    @mock.patch("mysql_rep_change.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.crt_slv_mst",
                mock.Mock(return_value=("NewMaster", False, None)))
    @mock.patch("mysql_rep_change.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mv_slv_to_new_mst")
    def test_move_fails(self, mock_move):

        """Function:  test_move_fails

        Description:  Test with move of slave to master fails.

        Arguments:

        """

        mock_move.return_value = (True, self.err_msg3)

        self.assertEqual(
            mysql_rep_change.move_slave(
                self.master, self.slaves, args=self.args2),
            (True, self.err_msg3))

    @mock.patch("mysql_rep_change.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.crt_slv_mst")
    def test_create_slave_fails(self, mock_crt):

        """Function:  test_sync_fails

        Description:  Test with create of slave fails.

        Arguments:

        """

        mock_crt.return_value = (None, True, self.err_msg2)

        self.assertEqual(mysql_rep_change.move_slave(
            self.master, self.slaves, args=self.args2), (True, self.err_msg2))

    @mock.patch("mysql_rep_change.fetch_slv")
    def test_fetch_slv_fails(self, mock_fetch):

        """Function:  test_fetch_slv_fails

        Description:  Test with fetching slave fails.

        Arguments:

        """

        mock_fetch.return_value = (None, True, self.err_msg)

        self.assertEqual(mysql_rep_change.move_slave(
            self.master, self.slaves, args=self.args2), (True, self.err_msg))


if __name__ == "__main__":
    unittest.main()