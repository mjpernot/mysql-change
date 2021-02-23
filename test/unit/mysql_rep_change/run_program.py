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


class MasterRep(object):

    """Class:  MasterRep

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


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

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
        self.rep_user = "RepUser"
        self.rep_japd = None
        self.extra_def_file = "FileName"
        self.conn = True
        self.conn_msg = None


def move_slave(master, slave, **kwargs):

    """Function:  move_slave

    Description:  move_slave function.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.

    """

    status = False
    msg = None
    args_array = dict(kwargs.get("args"))

    if master and slave and args_array:
        status = False

    return status, msg


def move_slave_up(master, slave, **kwargs):

    """Function:  move_slave_up

    Description:  move_slave_up function.

    Arguments:
        (input) master -> Master instance.
        (input) slave -> Slave instance.

    """

    status = True
    msg = "Error Message"
    args_array = dict(kwargs.get("args"))

    if master and slave and args_array:
        status = True

    return status, msg


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_master_slave_conn -> Test with no master and slave connection.
        test_two_no_slave_conn -> Test with two no slave connections.
        test_one_no_slave_conn -> Test with one no slave connection.
        test_no_master_conn -> Test with no master connection.
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

        self.err_msg = "Connection Error"
        self.args_array = {"-m": "master", "-n": "slaves"}
        self.args_array2 = {"-m": "master", "-n": "slaves", "-M": True}
        self.args_array3 = {"-m": "master", "-n": "slaves", "-M": True,
                            "-R": True}
        self.args_array4 = {"-m": "master", "-n": "slaves", "-S": True}
        self.func_dict = {"-M": move_slave, "-R": move_slave,
                          "-S": move_slave_up}
        self.master = MasterRep()
        self.master2 = MasterRep()
        self.master2.conn = False
        self.master2.conn_msg = self.err_msg
        self.slave = SlaveRep()
        self.slave2 = SlaveRep()
        self.slave3 = SlaveRep()
        self.slave3.conn = False
        self.slave3.conn_msg = self.err_msg
        self.slave4 = SlaveRep()
        self.slave4.conn = False
        self.slave4.conn_msg = self.err_msg
        self.slave_list = [self.slave, self.slave2]
        self.slave_list2 = [self.slave, self.slave2, self.slave3]
        self.slave_list3 = [self.slave, self.slave2, self.slave3, self.slave4]

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_no_master_slave_conn(self, mock_create):

        """Function:  test_no_master_slave_conn

        Description:  Test with no master and slave connection.

        Arguments:

        """

        mock_create.return_value = (self.master2, self.slave_list2)

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_change.run_program(self.args_array2,
                                                          self.func_dict))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_two_no_slave_conn(self, mock_create):

        """Function:  test_two_no_slave_conn

        Description:  Test with two no slave connections.

        Arguments:

        """

        mock_create.return_value = (self.master, self.slave_list3)

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_change.run_program(self.args_array2,
                                                          self.func_dict))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_one_no_slave_conn(self, mock_create):

        """Function:  test_one_no_slave_conn

        Description:  Test with one no slave connection.

        Arguments:

        """

        mock_create.return_value = (self.master, self.slave_list2)

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_change.run_program(self.args_array2,
                                                          self.func_dict))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_no_master_conn(self, mock_create):

        """Function:  test_no_master_conn

        Description:  Test with no master connection.

        Arguments:

        """

        mock_create.return_value = (self.master2, self.slave_list)

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_change.run_program(self.args_array2,
                                                          self.func_dict))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_with_option_fails(self, mock_create):

        """Function:  test_with_option_fails

        Description:  Test with option failing.

        Arguments:

        """

        mock_create.return_value = (self.master, self.slave_list)

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_change.run_program(self.args_array4,
                                                          self.func_dict))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_with_multiple_options(self, mock_create):

        """Function:  test_with_multiple_options

        Description:  Test with multiple options selected.

        Arguments:

        """

        mock_create.return_value = (self.master, self.slave_list)

        self.assertFalse(mysql_rep_change.run_program(self.args_array3,
                                                      self.func_dict))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_with_option(self, mock_create):

        """Function:  test_with_option

        Description:  Test with option selected.

        Arguments:

        """

        mock_create.return_value = (self.master, self.slave_list)

        self.assertFalse(mysql_rep_change.run_program(self.args_array2,
                                                      self.func_dict))

    @mock.patch("mysql_rep_change.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_change.create_instances")
    def test_no_option(self, mock_create):

        """Function:  test_no_option

        Description:  Test with no option selected.

        Arguments:

        """

        mock_create.return_value = (self.master, self.slave_list)

        self.assertFalse(mysql_rep_change.run_program(self.args_array,
                                                      self.func_dict))


if __name__ == "__main__":
    unittest.main()
