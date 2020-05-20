#!/usr/bin/python
# Classification (U)

"""Program:  mysql_rep_change.py

    Description:  Administration program for MySQL Replication system.  The
        program has a number of functions to allow moving a slave to under a
        slave/master or moving a slave to to under a slave/master and dropping
        the replication connection between the current master and the
        new slave/master, or moving a slave that is under a slave/master to the
        master that is hosting the slave/master.

    Warning:  This program will allow the changing of the slaves databases to
        new replication configurations, but it does not update the
        slave configuration files or creates new master configuration
        files.  This must be done outside the scope of this program.

    Usage:
        mysql_rep_change.py -d path -c file -s [path/]file [-M | -R |
            -C | -S] [-m {name | file} -n name] [-v | -h]

    Arguments:
        -c file => Current Master config file.  Is loaded as a python, do not
            include the .py extension with the name.  Required arg.
        -s file => Slave config file.  Will be a text file.  Include the
            file extension with the name.  Can include the path or use
            the -d option path.  Required arg.
        -d dir path => Directory path to the config files. Required arg.
        -M -> Move slave in a slave array to under another slave in the
            same slave array.
        -R -> Move slave in a slave array to under another slave in the
            same slave array and remove the replication connection
            between the current master and new master.
        -S -> Take a slave that is under a slave/master and move it to
            under the master that is hosting the slave/master
            (Topology:  Master -> Slave/Master -> Slave).
        -m name => Name of the new master or new Master config file.
        -n name => Name of a slave to be moved to the new master.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -M, -R, and -S are XOR arguments.
        NOTE 3:  The name for -m option is the server_name entry from the slave
            configuration file for the -M and -R options.  For the -S option
            the -m is a master configuration file name (minus .py extension).

    Notes:
        Database configuration file format (config/mysql_cfg.py.TEMPLATE):
            # Configuration file for {Database Name/Server}
            user = "USER"
            passwd = "PASSWORD"
            host = "IP_ADDRESS"
            serv_os = "Linux"
            name = "HOSTNAME"
            port = 3306
            cfg_file = "DIRECTORY_PATH/mysql.cnf"
            sid = SERVER_ID
            extra_def_file = "DIRECTORY_PATH/config/mysql.cfg"

            NOTE 1:  Include the cfg_file even if running remotely as the
                file will be used in future releases.

            NOTE 2:  In MySQL 5.6 - it now gives warning if password is
                passed on the command line.  To suppress this warning, will
                require the use of the --defaults-extra-file option
                (i.e. extra_def_file) in the database configuration file.
                See below for the defaults-extra-file format.

            configuration modules -> name is runtime dependent as it can be
                used to connect to different databases with different names.

            Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password="PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

            NOTE:  The socket information can be obtained from the my.cnf
                file under ~/mysql directory.

    Example:
        mysql_rep_change.py -c master -d config -s slaves.txt -M
            -m new_master_name -n slave_name

"""

# Libraries and Global Variables

# Standard
import sys

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.cmds_gen as cmds_gen
import lib.machine as machine
import mysql_lib.mysql_libs as mysql_libs
import mysql_lib.mysql_class as mysql_class
import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def is_slv_up(SLV, **kwargs):

    """Function:  is_slv_up

    Description:  Checks to see if the slave is running and whether there are
        any errors to report.

    Arguments:
        (input) SLV -> Class instance of slave.

    """

    if not SLV.is_slv_running():
        print("Error:  Slave on {0} is not running.".format(SLV.name))

        if SLV.is_slv_error():
            print("IO Error:  {0}:  {1}".format(SLV.io_err, SLV.io_msg))
            print("SQL Error:  {0}:  {1}".format(SLV.sql_err, SLV.sql_msg))


def fetch_slv(SLAVES, **kwargs):

    """Function:  fetch_slv

    Description:  Locates a slave in the slave array.

    Arguments:
        (input) SLAVE -> Slave instance array.
        (input) **kwargs:
            slv_mv -> Name of slave to be moved to new master.
        (output) SLV -> Class instance of slave.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    err_flag = False
    err_msg = None
    SLV = None

    SLV = mysql_libs.find_name(SLAVES, kwargs.get("slv_mv"))

    if not SLV:
        err_flag = True
        err_msg = "Error:  Slave %s was not found in slave array." \
                  % (kwargs.get("slv_mv"))

    return SLV, err_flag, err_msg


def crt_slv_mst(SLAVES, **kwargs):

    """Function:  crt_slv_mst

    Description:  Creates the new master from an existing slave within the
        slave array.  Does ensure the slave is not in read-only mode.

    Arguments:
        (input) SLAVE -> Slave instance array.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
        (output) NEW_MST -> Class instance of new master.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    err_flag = False
    err_msg = None
    NEW_MST = None

    SLV = mysql_libs.find_name(SLAVES, kwargs.get("new_mst"))

    if SLV:

        if gen_libs.is_true(SLV.read_only):
            err_flag = True
            err_msg = "Error:  New master %s is set to read-only mode." \
                      % (kwargs.get("new_mst"))

        # Assume slave is ready to be new master.
        else:
            NEW_MST = mysql_class.MasterRep(SLV.name, SLV.server_id,
                                            SLV.sql_user, SLV.sql_pass,
                                            SLV.machine, SLV.host, SLV.port,
                                            SLV.defaults_file)

    else:
        err_flag = True
        err_msg = "Error: Slave(new master) %s was not found in slave array." \
                  % (kwargs.get("new_mst"))

    return NEW_MST, err_flag, err_msg


def mv_slv_to_new_mst(MASTER, SLAVES, NEW_MST, SLV_MV, **kwargs):

    """Function:  mv_slv_to_new_mst

    Description:  Moves the slave to the new master, but first syncs up current
        master with the slave and the new master before running a
        Change Master To command.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVES -> Slave instance array.
        (input) NEW_MST -> Class instance of new master.
        (input) SLV_MV -> Class instance of slave to be moved.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    for SVR in [mysql_libs.find_name(SLAVES, kwargs.get("new_mst")), SLV_MV]:

        err_flag, err_msg = mysql_libs.sync_rep_slv(MASTER, SVR)

        if err_flag:
            break

    # If the loop completes, then "Change Master To" can be ran.
    else:
        # Get latest log position.
        NEW_MST.upd_mst_status()
        mysql_libs.change_master_to(NEW_MST, SLV_MV)

    mysql_libs.chg_slv_state([mysql_libs.find_name(SLAVES,
                                                   kwargs.get("new_mst")),
                              SLV_MV], "start")

    return err_flag, err_msg


def move_slave(MASTER, SLAVES, **kwargs):

    """Function:  move_slave

    Description:  Calls the functions to setup the new master, locate the slave
        to be moved, and moves the slave to the new master.  Used to
        setup the new master from existing slave array and whether to
        drop the rep connection between the old master and new master.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVES -> Slave instance array.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
            slv_mv -> Name of slave to be moved to new master.
            args -> Array of command line options and values.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    SLV_MV, err_flag, err_msg = fetch_slv(SLAVES, **kwargs)

    if err_flag:
        return err_flag, err_msg

    NEW_MST, err_flag, err_msg = crt_slv_mst(SLAVES, **kwargs)

    if err_flag:
        return err_flag, err_msg

    err_flag, err_msg = mv_slv_to_new_mst(MASTER, SLAVES, NEW_MST, SLV_MV,
                                          **kwargs)

    if err_flag:
        cmds_gen.disconnect(NEW_MST)
        return err_flag, err_msg

    is_slv_up(SLV_MV)

    if "-R" in kwargs.get("args"):
        SLV_MST = mysql_libs.find_name(SLAVES, kwargs.get("new_mst"))
        mysql_libs.chg_slv_state([SLV_MST], "stop")
        mysql_libs.reset_slave(SLV_MST)

    else:
        is_slv_up(mysql_libs.find_name(SLAVES, kwargs.get("new_mst")))

    cmds_gen.disconnect(NEW_MST)

    return err_flag, err_msg


def move_slave_up(MASTER, SLAVES, **kwargs):

    """Function:  move_slave_up

    Description:  Find the slave that will be moved, creates the new and slave
        master instances, sync up the databases between new master,
        slave/master and slave and then move the slave from the
        slave/master to the new master.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVES -> Slave instance array.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
            slv_mv -> Name of slave to be moved to new master.
            args -> Array of command line options and values.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    SLV_MV, err_flag, err_msg = fetch_slv(SLAVES, **kwargs)

    if err_flag:
        return err_flag, err_msg

    NEW_MST = mysql_libs.create_instance(kwargs.get("new_mst"),
                                         kwargs.get("args")["-d"],
                                         mysql_class.MasterRep)

    SLV_MST = mysql_class.SlaveRep(MASTER.name, MASTER.server_id,
                                   MASTER.sql_user, MASTER.sql_pass,
                                   MASTER.machine, MASTER.host, MASTER.port,
                                   MASTER.defaults_file)

    err_flag, err_msg = mysql_libs.sync_rep_slv(NEW_MST, SLV_MST)

    if err_flag:
        cmds_gen.disconnect(NEW_MST, SLV_MST)
        return err_flag, err_msg

    err_flag, err_msg = \
        mysql_libs.sync_rep_slv(MASTER,
                                mysql_libs.find_name(SLAVES,
                                                     kwargs.get("slv_mv")))

    if err_flag:
        cmds_gen.disconnect(NEW_MST, SLV_MST)
        return err_flag, err_msg

    mysql_libs.change_master_to(NEW_MST, SLV_MV)
    cmds_gen.disconnect(NEW_MST, SLV_MST)
    mysql_libs.chg_slv_state([SLV_MV, SLV_MST], "start")
    is_slv_up(SLV_MV)
    is_slv_up(SLV_MST)

    return err_flag, err_msg


def create_instances(args_array, **kwargs):

    """Function:  create_instances

    Description:  Create a Master_Rep instance for master and Slave_Rep
        instances for slaves.  Slave instances will be appended to an array.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (output) MASTER -> Master instance.
        (output) SLAVE -> Slave instance array.

    """

    MASTER = mysql_libs.create_instance(args_array["-c"], args_array["-d"],
                                        mysql_class.MasterRep)
    SLAVES = []

    slv_array = cmds_gen.create_cfg_array(args_array["-s"],
                                          cfg_path=args_array["-d"])

    SLAVES = mysql_libs.create_slv_array(slv_array)

    return MASTER, SLAVES


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    MASTER, SLAVES = create_instances(args_array)

    if MASTER and SLAVES:

        for opt in args_array:

            if opt in func_dict:

                err_flag, err_msg = func_dict[opt](MASTER, SLAVES,
                                                   new_mst=args_array["-m"],
                                                   slv_mv=args_array["-n"],
                                                   args=args_array)

                cmds_gen.disconnect(MASTER, SLAVES)

                if err_flag:
                    sys.exit(err_msg)

    else:
        cmds_gen.disconnect(MASTER, SLAVES)
        sys.exit("Error:  Master and/or Slaves instances not created.")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_con_req_list -> contains the options that require other options.
        opt_req_list -> contains the options that are required for the program.
        opt_val_list -> contains options which require values.
        opt_xor_dict -> contains dict with key that is xor with it's values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d"]
    func_dict = {"-M": move_slave, "-R": move_slave, "-S": move_slave_up}
    opt_con_req_list = {"-M": ["-m", "-n"], "-R": ["-m", "-n"],
                        "-S": ["-m", "-n"]}
    opt_req_list = ["-c", "-d", "-s"]
    opt_val_list = ["-c", "-d", "-m", "-n", "-s"]
    opt_xor_dict = {"-M": ["-R", "-S"], "-R": ["-M", "-S"], "-S": ["-M", "-R"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message):
        if not arg_parser.arg_require(args_array, opt_req_list) \
           and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
           and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
           and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
            run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
