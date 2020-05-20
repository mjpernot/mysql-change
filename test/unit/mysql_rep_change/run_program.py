#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/run_program.py

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


def move_slave(master, slave, **kwargs):

    """Function:  move_slave

    Description:  move_slave function.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.

    """

    return False, None


def move_slave_up(master, slave, **kwargs):

    """Function:  move_slave_up

    Description:  move_slave_up function.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.

    """

    return True, "Error Message"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_master -> Test with no master instance.
        test_with_option_fails -> Test with option failing.
        test_with_multiple_options -> Test with multiple options selected.
        test_with_option -> Test with option selected.
        test_no_option -> Test with no option selected.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-m": "master", "-n": "slaves"}
        self.args_array2 = {"-m": "master", "-n": "slaves", "-M": True}
        self.args_array3 = {"-m": "master", "-n": "slaves", "-M": True,
                            "-R": True}
        self.args_array4 = {"-m": "master", "-n": "slaves", "-S": True}
        self.func_dict = {"-M": move_slave, "-R": move_slave,
                          "-S": move_slave_up}

    @mock.patch("mysql_rep_change.sys.exit", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances",
                mock.Mock(return_value=(None, "Slave")))
    def test_no_master(self):

        """Function:  test_no_master

        Description:  Test with no master instance.

        Arguments:

        """

        self.assertFalse(mysql_rep_change.run_program(self.args_array,
                                                      self.func_dict))

    @mock.patch("mysql_rep_change.sys.exit", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances",
                mock.Mock(return_value=("Master", "Slave")))
    def test_with_option_fails(self):

        """Function:  test_with_option_fails

        Description:  Test with option failing.

        Arguments:

        """

        self.assertFalse(mysql_rep_change.run_program(self.args_array4,
                                                      self.func_dict))

    @mock.patch("mysql_rep_change.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances",
                mock.Mock(return_value=("Master", "Slave")))
    def test_with_multiple_options(self):

        """Function:  test_with_multiple_options

        Description:  Test with multiple options selected.

        Arguments:

        """

        self.assertFalse(mysql_rep_change.run_program(self.args_array3,
                                                      self.func_dict))

    @mock.patch("mysql_rep_change.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances",
                mock.Mock(return_value=("Master", "Slave")))
    def test_with_option(self):

        """Function:  test_with_option

        Description:  Test with option selected.

        Arguments:

        """

        self.assertFalse(mysql_rep_change.run_program(self.args_array2,
                                                      self.func_dict))

    @mock.patch("mysql_rep_change.create_instances",
                mock.Mock(return_value=("Master", "Slave")))
    def test_no_option(self):

        """Function:  test_no_option

        Description:  Test with no option selected.

        Arguments:

        """

        self.assertFalse(mysql_rep_change.run_program(self.args_array,
                                                      self.func_dict))


if __name__ == "__main__":
    unittest.main()
