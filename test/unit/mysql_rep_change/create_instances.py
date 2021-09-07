#!/usr/bin/python
# Classification (U)

"""Program:  create_instances.py

    Description:  Unit testing of create_instances in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/create_instances.py

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
        test_create_instances

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = Cfg()
        self.master = MasterRep()
        self.args_array = {"-c": "mysql_cfg", "-d": "config", "-s": "slave"}
        self.name = "Server_Name"

    @mock.patch("mysql_rep_change.mysql_libs.create_slv_array",
                mock.Mock(return_value="SlaveArray"))
    @mock.patch("mysql_rep_change.gen_libs.create_cfg_array",
                mock.Mock(return_value=[]))
    @mock.patch("mysql_rep_change.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_change.gen_libs.load_module")
    @mock.patch("mysql_rep_change.mysql_class.MasterRep")
    def test_create_instances(self, mock_inst, mock_cfg, mock_trans):

        """Function:  test_create_instances

        Description:  Test create_instances function.

        Arguments:

        """

        mock_inst.return_value = self.master
        mock_cfg.return_value = self.cfg
        mock_trans.return_value = []

        master, slaves = mysql_rep_change.create_instances(self.args_array)

        self.assertEqual((master.name, slaves), (self.name, "SlaveArray"))


if __name__ == "__main__":
    unittest.main()
