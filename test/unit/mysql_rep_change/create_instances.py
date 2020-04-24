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

        self.args_array = {"-c": "mysql_cfg", "-d": "config", "-s": "slave"}

    @mock.patch("mysql_rep_change.mysql_libs.create_slv_array",
                mock.Mock(return_value="SlaveArray"))
    @mock.patch("mysql_rep_change.cmds_gen.create_cfg_array",
                mock.Mock(return_value=[]))
    @mock.patch("mysql_rep_change.mysql_libs.create_instance",
                mock.Mock(return_value="Master"))
    def test_create_instances(self):

        """Function:  test_create_instances

        Description:  Test create_instances function.

        Arguments:

        """

        self.assertEqual(mysql_rep_change.create_instances(
            self.args_array), ("Master", "SlaveArray"))


if __name__ == "__main__":
    unittest.main()
