#!/usr/bin/python
# Classification (U)

"""Program:  move_slave_up.py

    Description:  Unit testing of move_slave_up in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/move_slave_up.py

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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__
        upd_mst_status
        connect

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
        self.rep_user = "RepUser"
        self.rep_japd = None
        self.defaults_file = None
        self.conn = True
        self.conn_msg = None

    def upd_mst_status(self):

        """Method:  upd_mst_status

        Description:  upd_mst_status method.

        Arguments:

        """

        return True

    def connect(self, silent=False):

        """Method:  connect

        Description:  connect method.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        connect

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
        self.rep_user = "RepUser"
        self.rep_japd = None
        self.defaults_file = None
        self.conn = True
        self.conn_msg = None

    def connect(self, silent=False):

        """Method:  connect

        Description:  connect method.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status


class Cfg(object):

    """Class:  Cfg

    Description:  Stub holder for configuration file.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "name"
        self.sid = 10
        self.user = "user"
        self.japd = None
        self.serv_os = "Linux"
        self.host = "hostname"
        self.port = 3306
        self.cfg_file = "cfg_file"
        self.rep_user = "repuser"
        self.rep_japd = None


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_slave_new_master
        test_no_slave_master
        test_no_new_master
        test_slave_moved
        test_find_slave_fails
        test_sync_slave_fails
        test_fetch_slv_fails

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = Cfg()
        self.master = MasterRep()
        self.slave = SlaveRep()
        self.slaves = [self.slave]
        self.err_msg = "Error: Sync Rep Failed"
        self.err_msg2 = "Error: Sync Replication2 Failed"
        self.err_msg3 = "Connection error"
        self.err_msg4 = "Detected problem in one of the connections"
        self.new_mst = "NewMaster"
        self.args = {"-d": True}

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mysql_class.SlaveRep")
    @mock.patch("mysql_rep_change.gen_libs.load_module")
    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    def test_no_slave_new_master(self, mock_inst, mock_cfg, mock_slv):

        """Function:  test_no_slave_new_master

        Description:  Test with no new & slave master connection.

        Arguments:

        """

        self.master.conn = False
        self.master.conn_msg = self.err_msg3
        self.slave.conn = False
        self.slave.conn_msg = self.err_msg3

        mock_inst.return_value = self.master
        mock_cfg.return_value = self.cfg
        mock_slv.return_value = self.slave

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_change.move_slave_up(
                    self.master, self.slaves, args=self.args,
                    new_mst=self.new_mst), (True, self.err_msg4))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mysql_class.SlaveRep")
    @mock.patch("mysql_rep_change.gen_libs.load_module")
    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    def test_no_slave_master(self, mock_inst, mock_cfg, mock_slv):

        """Function:  test_no_slave_master

        Description:  Test with no slave master connection fails.

        Arguments:

        """

        self.slave.conn = False
        self.slave.conn_msg = self.err_msg3

        mock_inst.return_value = self.master
        mock_cfg.return_value = self.cfg
        mock_slv.return_value = self.slave

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_change.move_slave_up(
                    self.master, self.slaves, args=self.args,
                    new_mst=self.new_mst), (True, self.err_msg4))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mysql_class.SlaveRep")
    @mock.patch("mysql_rep_change.gen_libs.load_module")
    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    def test_no_new_master(self, mock_inst, mock_cfg, mock_slv):

        """Function:  test_no_new_master

        Description:  Test with no new master connection fails.

        Arguments:

        """

        self.master.conn = False
        self.master.conn_msg = self.err_msg3

        mock_inst.return_value = self.master
        mock_cfg.return_value = self.cfg
        mock_slv.return_value = self.slave

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_rep_change.move_slave_up(
                    self.master, self.slaves, args=self.args,
                    new_mst=self.new_mst), (True, self.err_msg4))

    @mock.patch("mysql_rep_change.is_slv_up", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.chg_slv_state",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.change_master_to",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mysql_libs.find_name",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_class.SlaveRep")
    @mock.patch("mysql_rep_change.gen_libs.load_module")
    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    @mock.patch("mysql_rep_change.mysql_libs.sync_rep_slv")
    def test_slave_moved(self, mock_sync, mock_inst, mock_cfg, mock_slv):

        """Function:  test_slave_moved

        Description:  Test with slave moved up.

        Arguments:

        """

        mock_sync.side_effect = [(False, None), (False, None)]
        mock_inst.return_value = self.master
        mock_cfg.return_value = self.cfg
        mock_slv.return_value = self.slave

        self.assertEqual(
            mysql_rep_change.move_slave_up(
                self.master, self.slaves, args=self.args,
                new_mst=self.new_mst), (False, None))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mysql_libs.find_name",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_class.SlaveRep")
    @mock.patch("mysql_rep_change.gen_libs.load_module")
    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    @mock.patch("mysql_rep_change.mysql_libs.sync_rep_slv")
    def test_find_slave_fails(self, mock_sync, mock_inst, mock_cfg, mock_slv):

        """Function:  test_find_slave_fails

        Description:  Test with find of slave fails.

        Arguments:

        """

        mock_sync.side_effect = [(False, None), (True, self.err_msg2)]
        mock_inst.return_value = self.master
        mock_cfg.return_value = self.cfg
        mock_slv.return_value = self.slave

        self.assertEqual(
            mysql_rep_change.move_slave_up(
                self.master, self.slaves, args=self.args,
                new_mst=self.new_mst), (True, self.err_msg2))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.mysql_libs.fetch_slv",
                mock.Mock(return_value=("SlaveMove", False, None)))
    @mock.patch("mysql_rep_change.mysql_class.SlaveRep")
    @mock.patch("mysql_rep_change.gen_libs.load_module")
    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    @mock.patch("mysql_rep_change.mysql_libs.sync_rep_slv")
    def test_sync_slave_fails(self, mock_sync, mock_inst, mock_cfg, mock_slv):

        """Function:  test_sync_slave_fails

        Description:  Test with sync up of slave fails.

        Arguments:

        """

        mock_sync.return_value = (True, self.err_msg)
        mock_inst.return_value = self.master
        mock_cfg.return_value = self.cfg
        mock_slv.return_value = self.slave

        self.assertEqual(
            mysql_rep_change.move_slave_up(
                self.master, self.slaves, args=self.args,
                new_mst=self.new_mst), (True, self.err_msg))

    @mock.patch("mysql_rep_change.mysql_libs.fetch_slv")
    def test_fetch_slv_fails(self, mock_fetch):

        """Function:  test_fetch_slv_fails

        Description:  Test with fetching slave fails.

        Arguments:

        """

        mock_fetch.return_value = (None, True, self.err_msg)

        self.assertEqual(mysql_rep_change.move_slave_up(
            self.master, self.slaves, args=self.args), (True, self.err_msg))


if __name__ == "__main__":
    unittest.main()
