#!/usr/bin/python
# Classification (U)

"""Program:  is_slv_up.py

    Description:  Unit testing of is_slv_up in mysql_rep_change.py.

    Usage:
        test/unit/mysql_rep_change/is_slv_up.py

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
        is_slv_running -> is_slv_running method.
        is_slv_error -> is_slv_error method.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.running = True
        self.slv_error = True
        self.name = "Server_Name"
        self.io_err = "IO Error"
        self.io_msg = "IO Message"
        self.sql_err = "SQL Error"
        self.sql_msg = "SQL Message"

    def is_slv_running(self):

        """Method:  is_slv_running

        Description:  is_slv_running method.

        Arguments:

        """

        return self.running

    def is_slv_error(self):

        """Method:  is_slv_error

        Description:  is_slv_error method.

        Arguments:

        """

        return self.slv_error


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_slave_errors -> Test with slave errors.
        test_slave_not_running -> Test with slave not running.
        test_slave_running -> Test with slave running.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()

    def test_slave_errors(self):

        """Function:  test_slave_errors

        Description:  Test with slave errors.

        Arguments:

        """

        self.slave.running = False

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_change.is_slv_up(self.slave))

    def test_slave_not_running(self):

        """Function:  test_slave_not_running

        Description:  Test with slave not running.

        Arguments:

        """

        self.slave.running = False
        self.slave.slv_error = False

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_change.is_slv_up(self.slave))

    def test_slave_running(self):

        """Function:  test_slave_running

        Description:  Test with slave running.

        Arguments:

        """

        self.assertFalse(mysql_rep_change.is_slv_up(self.slave))


if __name__ == "__main__":
    unittest.main()
