#!/usr/bin/python
# Classification (U)

"""Program:  mv_slv_to_new_mst.py

    Description:  Unit testing of mv_slv_to_new_mst in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/mv_slv_to_new_mst.py

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
        __init__
        upd_mst_status

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
        __init__

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
        setUp
        test_sync_fails
        test_sync_slaves

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.slave = SlaveRep()
        self.slaves = [self.slave]
        self.new_master = MasterRep()
        self.slv_mv = SlaveRep()
        self.new_mst = "SlaveName"
        self.err_msg = "Error: Sync failed"

    @mock.patch("mysql_rep_change.mysql_libs.sync_rep_slv")
    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_sync_fails(self, mock_find, mock_sync):

        """Function:  test_sync_fails

        Description:  Test with syncing between slaves fails.

        Arguments:

        """

        mock_find.return_value = self.slave
        mock_sync.return_value = (True, self.err_msg)

        self.assertEqual(mysql_rep_change.mv_slv_to_new_mst(
            self.master, self.slaves, self.new_master, self.slv_mv,
            new_mst=self.new_mst), (True, self.err_msg))

    @mock.patch("mysql_rep_change.mysql_libs.chg_slv_state",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.change_master_to",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.sync_rep_slv",
                mock.Mock(return_value=(False, None)))
    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_sync_slaves(self, mock_find):

        """Function:  test_sync_slaves

        Description:  Test with syncing up slaves successfully.

        Arguments:

        """

        mock_find.return_value = self.slave

        self.assertEqual(mysql_rep_change.mv_slv_to_new_mst(
            self.master, self.slaves, self.new_master, self.slv_mv,
            new_mst=self.new_mst), (False, None))


if __name__ == "__main__":
    unittest.main()
