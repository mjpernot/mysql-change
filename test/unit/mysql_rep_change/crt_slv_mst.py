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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_change                         # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class MasterRep():                                      # pylint:disable=R0903

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__
        connect

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Master_Server_Name"
        self.read_only = "OFF"
        self.server_id = 10
        self.sql_user = "User"
        self.sql_pass = None
        self.machine = "Linux"
        self.host = "HostName"
        self.port = 3306
        self.defaults_file = None
        self.rep_user = "RepUser"
        self.rep_japd = None
        self.extra_def_file = "FileName"
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


class SlaveRep():                                       # pylint:disable=R0903

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
        self.defaults_file = None
        self.rep_user = "RepUser"
        self.rep_japd = None
        self.extra_def_file = "FileName"
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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_new_master_conn
        test_no_found_slave
        test_readonly_slave
        test_found_slave

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()
        self.master = MasterRep()
        self.name = "Master_Server_Name"
        self.slaves = [self.slave]
        self.new_mst = "SlaveName"
        self.result_msg = \
            "Error:  New master SlaveName is set to read-only mode."
        self.result_msg2 = \
            "Error: Slave(new master) SlaveName was not found in slave array."
        self.result_msg3 = "Detected problem in new master connection"

    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_no_new_master_conn(self, mock_find, mock_mst):

        """Function:  test_no_new_master_conn

        Description:  Test with no new master conection failure.

        Arguments:

        """

        self.master.conn = False
        self.master.conn_msg = "Error Connection"

        mock_find.return_value = self.slave
        mock_mst.return_value = self.master

        with gen_libs.no_std_out():
            master, err_flag, err_msg = mysql_rep_change.crt_slv_mst(
                self.slaves, new_mst=self.new_mst)

        self.assertEqual((master.name, err_flag, err_msg),
                         (self.name, True, self.result_msg3))

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

    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    @mock.patch("mysql_rep_change.mysql_libs.find_name")
    def test_found_slave(self, mock_find, mock_mst):

        """Function:  test_found_slave

        Description:  Test with slave found.

        Arguments:

        """

        mock_find.return_value = self.slave
        mock_mst.return_value = self.master

        master, err_flag, err_msg = mysql_rep_change.crt_slv_mst(
            self.slaves, new_mst=self.new_mst)

        self.assertEqual((master.name, err_flag, err_msg),
                         (self.name, False, None))


if __name__ == "__main__":
    unittest.main()
