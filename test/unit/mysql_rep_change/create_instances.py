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
import lib.gen_libs as gen_libs
import mysql_rep_change
import version

__version__ = version.__version__


class MasterRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__ -> Class initialization.
        connect -> connect method.

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

    def connect(self):

        """Method:  connect

        Description:  connect method.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_create_instances -> Test create_instances function.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = MasterRep()
        self.args_array = {"-c": "mysql_cfg", "-d": "config", "-s": "slave"}
        self.name = "Server_Name"

    @mock.patch("mysql_rep_change.mysql_libs.create_slv_array",
                mock.Mock(return_value="SlaveArray"))
    @mock.patch("mysql_rep_change.cmds_gen.create_cfg_array",
                mock.Mock(return_value=[]))
    @mock.patch("mysql_rep_change.mysql_libs.create_instance")
    def test_create_instances(self, mock_inst):

        """Function:  test_create_instances

        Description:  Test create_instances function.

        Arguments:

        """

        mock_inst.return_value = self.master

        master, slaves = mysql_rep_change.create_instances(self.args_array)

        self.assertEqual((master.name, slaves), (self.name, "SlaveArray"))


if __name__ == "__main__":
    unittest.main()
