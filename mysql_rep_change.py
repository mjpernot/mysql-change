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
        files.  This must be done manually outside the scope of this program.

    Usage:
        mysql_rep_change.py -c cfg_file -d path -s [path/]file
            {-M -m new_master_name -n slave_name |
             -R -m new_master_name -n slave_name |
             -S -m new_master -n slave_name}
            [-y flavor_id]
            [-v | -h]

    Arguments:
        -c cfg_file => Current Master config file.  Is loaded as a python, do
            not include the .py extension with the name.  Required arg.
        -s [path/]file => Slave config file.  Will be a text file.  Include the
            file extension with the name.  Can include the path or use the -d
            option path.  Required arg.
        -d dir path => Directory path to the config files. Required arg.

        -M -> Move slave in a slave array to under another slave in the same
                slave array.
            -m new_master_name => Name of the new master from slave cfg file.
            -n slave_name => Name of a slave to be moved to the new master.

        -R -> Move slave in a slave array to under another slave in the same
                slave array and remove the replication connection between the
                current master and new master.
            -m new_master_name => Name of the new master from slave cfg file.
            -n slave_name => Name of a slave to be moved to the new master.

        -S -> Take a slave that is under a slave/master and move it to under
                the master that is hosting the slave/master
                (Current Topology:  New_Master -> Slave1/Master -> Slave2)
                (New Topology:  New_Master -> Slave1
                                New_Master -> Slave2)
            -m new_master => Name of the New_Master config file.
            -n slave_name => Name of a slave to be moved to the New_Master.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -M, -R, and -S are XOR arguments.
        NOTE 3:  -M and -R options:  The name for -m option is the server_name
            entry from the slave configuration file.
        NOTE 4:  -S option:  The -m is a master configuration file name
            (minus .py extension).

    Notes:
        Database configuration file format (config/mysql_cfg.py.TEMPLATE):
            # Configuration file for Database Server.
            user = "USER"
            japd = "PSWORD"
            rep_user = REP_USER
            rep_japd = REP_PSWORD
            host = "HOST_IP"
            name = "HOST_NAME"
            sid = SERVER_ID
            extra_def_file = "PYTHON_PROJECT/config/mysql.cfg"
            serv_os = "Linux"
            port = 3306
            cfg_file = "DIRECTORY_PATH/my.cnf"

        NOTE 1:  Include the cfg_file even if running remotely as the file will
            be used in future releases.

        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the defaults-extra-file
            format.

        configuration modules -> name is runtime dependent as it can be used to
            connect to different databases with different names.

        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password="PASSWORD"
            socket="DIRECTORY_PATH/mysqld.sock"

        NOTE 1:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.

        NOTE 2:  The --defaults-extra-file option will be overridden if there
            is a ~/.my.cnf or ~/.mylogin.cnf file located in the home directory
            of the user running this program.  The extras file will in effect
            be ignored.

        Slave configuration file format (config/slave.txt.TEMPLATE)
            # Slave configuration
            user = USER
            japd = PSWORD
            rep_user = REP_USER
            rep_japd = REP_PSWORD
            host = HOST_IP
            name = HOST_NAME
            sid = SERVER_ID
            cfg_file = None
            port = 3306
            serv_os = Linux
            extra_def_file = DIRECTORY_PATH/mysql.cfg

        NOTE:  Create a Slave configration section for each slave.

    Example:
        mysql_rep_change.py -c master -d config -s slaves.txt -M
            -m new_master -n slave_name

"""

# Libraries and Global Variables

# Standard
import sys

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.cmds_gen as cmds_gen
import lib.gen_class as gen_class
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


def is_slv_up(slv):

    """Function:  is_slv_up

    Description:  Checks to see if the slave is running and whether there are
        any errors to report.

    Arguments:
        (input) slv -> Class instance of slave.

    """

    if not slv.is_slv_running():
        print("Error:  Slave on {0} is not running.".format(slv.name))

        if slv.is_slv_error():
            print("IO Error:  {0}:  {1}".format(slv.io_err, slv.io_msg))
            print("SQL Error:  {0}:  {1}".format(slv.sql_err, slv.sql_msg))


def crt_slv_mst(slaves, **kwargs):

    """Function:  crt_slv_mst

    Description:  Creates the new master from an existing slave within the
        slave array.  Does ensure the slave is not in read-only mode.

    Arguments:
        (input) slaves -> Slave instance array.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
        (output) new_master -> Class instance of new master.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    slaves = list(slaves)
    err_flag = False
    err_msg = None
    new_master = None
    slv = mysql_libs.find_name(slaves, kwargs.get("new_mst"))

    if slv:

        if gen_libs.is_true(slv.read_only):
            err_flag = True
            err_msg = "Error:  New master %s is set to read-only mode." \
                      % (kwargs.get("new_mst"))

        # Assume slave is ready to be new master.
        else:
            new_master = mysql_class.MasterRep(
                slv.name, slv.server_id, slv.sql_user, slv.sql_pass,
                os_type=slv.machine, host=slv.host, port=slv.port,
                defaults_file=slv.defaults_file,
                extra_def_file=slv.extra_def_file, rep_user=slv.rep_user,
                rep_japd=slv.rep_japd)
            new_master.connect(silent=True)

            if new_master.conn_msg:
                err_flag = True
                err_msg = "Detected problem in new master connection"
                print("Error:  Connection problem for new master.")
                print("\tNew Master:  %s" % (new_master.conn_msg))

    else:
        err_flag = True
        err_msg = "Error: Slave(new master) %s was not found in slave array." \
                  % (kwargs.get("new_mst"))

    return new_master, err_flag, err_msg


def mv_slv_to_new_mst(master, slaves, new_master, slave_move, **kwargs):

    """Function:  mv_slv_to_new_mst

    Description:  Moves the slave to the new master, but first syncs up current
        master with the slave and the new master before running a
        Change Master To command.

    Arguments:
        (input) master -> Master class instance.
        (input) slaves -> Slave instance array.
        (input) new_master -> Class instance of new master.
        (input) slave_move -> Class instance of slave to be moved.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    slaves = list(slaves)

    for svr in [mysql_libs.find_name(slaves, kwargs.get("new_mst")),
                slave_move]:

        err_flag, err_msg = mysql_libs.sync_rep_slv(master, svr)

        if err_flag:
            break

    # Only run if loop completes without error.
    else:
        # Get latest log position.
        new_master.upd_mst_status()
        mysql_libs.change_master_to(new_master, slave_move)

        mysql_libs.chg_slv_state(
            [mysql_libs.find_name(slaves, kwargs.get("new_mst")), slave_move],
            "start")

    return err_flag, err_msg


def move_slave(master, slaves, **kwargs):

    """Function:  move_slave

    Description:  Calls the functions to setup the new master, locate the slave
        to be moved, and moves the slave to the new master.  Used to
        setup the new master from existing slave array and whether to
        drop the rep connection between the old master and new master.

    Arguments:
        (input) master -> Master class instance.
        (input) slaves -> Slave instance array.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
            slv_mv -> Name of slave to be moved to new master.
            args -> Array of command line options and values.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    args_array = dict(kwargs.get("args"))
    slaves = list(slaves)
    slave_move, err_flag, err_msg = mysql_libs.fetch_slv(slaves,
                                                         kwargs.get("slv_mv"))

    if not err_flag:
        new_master, err_flag, err_msg = crt_slv_mst(slaves, **kwargs)

        if not err_flag:
            err_flag, err_msg = mv_slv_to_new_mst(
                master, slaves, new_master, slave_move, **kwargs)

            if not err_flag:
                is_slv_up(slave_move)

                if "-R" in args_array:
                    slv_mst = mysql_libs.find_name(slaves,
                                                   kwargs.get("new_mst"))
                    mysql_libs.chg_slv_state([slv_mst], "stop")
                    mysql_libs.reset_slave(slv_mst)

                else:
                    is_slv_up(mysql_libs.find_name(slaves,
                                                   kwargs.get("new_mst")))

            mysql_libs.disconnect(new_master)

    return err_flag, err_msg


def move_slave_up(master, slaves, **kwargs):

    """Function:  move_slave_up

    Description:  Find the slave that will be moved, creates the new and slave
        master instances, sync up the databases between new master,
        slave/master and slave and then move the slave from the
        slave/master to the new master.

    Arguments:
        (input) master -> Master class instance.
        (input) slaves -> Slave instance array.
        (input) **kwargs:
            new_mst -> Name of slave to be the new master.
            slv_mv -> Name of slave to be moved to new master.
            args -> Array of command line options and values.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    args_array = dict(kwargs.get("args"))
    slaves = list(slaves)
    slave_move, err_flag, err_msg = mysql_libs.fetch_slv(slaves,
                                                         kwargs.get("slv_mv"))

    if err_flag:
        return err_flag, err_msg

    cfg = gen_libs.load_module(kwargs.get("new_mst"), args_array["-d"])
    new_master = mysql_class.MasterRep(
        cfg.name, cfg.sid, cfg.user, cfg.japd,
        os_type=getattr(machine, cfg.serv_os)(), host=cfg.host, port=cfg.port,
        defaults_file=cfg.cfg_file,
        extra_def_file=cfg.__dict__.get("extra_def_file", None),
        rep_user=cfg.rep_user, rep_japd=cfg.rep_japd)
    new_master.connect(silent=True)
    slv_master = mysql_class.SlaveRep(
        master.name, master.server_id, master.sql_user, master.sql_pass,
        os_type=master.machine, host=master.host, port=master.port,
        defaults_file=master.defaults_file, rep_user=master.rep_user,
        rep_japd=master.rep_japd)
    slv_master.connect(silent=True)

    if new_master.conn_msg or slv_master.conn_msg:
        err_flag = True
        err_msg = "Detected problem in one of the connections"

        print("Error:  Connection problem for new master/slave master.")
        print("\tNew Master:  %s" % (new_master.conn_msg))
        print("\tSlave Master:  %s" % (slv_master.conn_msg))

        if new_master.conn:
            mysql_libs.disconnect(new_master)

        if slv_master.conn:
            mysql_libs.disconnect(slv_master)

    else:
        err_flag, err_msg = mysql_libs.sync_rep_slv(new_master, slv_master)

        if not err_flag:
            err_flag, err_msg = mysql_libs.sync_rep_slv(
                master, mysql_libs.find_name(slaves, kwargs.get("slv_mv")))

            if not err_flag:
                mysql_libs.change_master_to(new_master, slave_move)
                mysql_libs.chg_slv_state([slave_move, slv_master], "start")
                is_slv_up(slave_move)
                is_slv_up(slv_master)

        mysql_libs.disconnect(new_master, slv_master)

    return err_flag, err_msg


def create_instances(args_array):

    """Function:  create_instances

    Description:  Create a Master_Rep instance for master and Slave_Rep
        instances for slaves.  Slave instances will be appended to an array.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (output) master -> Master instance.
        (output) slave -> Slave instance list.

    """

    args_array = dict(args_array)
    cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])
    master = mysql_class.MasterRep(
        cfg.name, cfg.sid, cfg.user, cfg.japd,
        os_type=getattr(machine, cfg.serv_os)(), host=cfg.host, port=cfg.port,
        defaults_file=cfg.cfg_file,
        extra_def_file=cfg.__dict__.get("extra_def_file", None),
        rep_user=cfg.rep_user, rep_japd=cfg.rep_japd)
    master.connect(silent=True)
    slaves = []
    slv_array = cmds_gen.create_cfg_array(args_array["-s"],
                                          cfg_path=args_array["-d"])
    slaves = mysql_libs.create_slv_array(slv_array)

    return master, slaves


def run_program(args_array, func_dict):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    master, slaves = create_instances(args_array)

    if slaves and not master.conn_msg \
       and not [False for item in slaves if item.conn_msg]:

        # Intersect args_array and func_dict to call function.
        for item in set(args_array.keys()) & set(func_dict.keys()):
            err_flag, err_msg = func_dict[item](
                master, slaves, new_mst=args_array["-m"],
                slv_mv=args_array["-n"], args=args_array)

            if err_flag:
                print(err_msg)
                break

        mysql_libs.disconnect(master, slaves)

    else:
        print("Error:  Connection problem for master/slaves.")
        print("\tMaster:  %s" % (master.conn_msg))

        if master.conn:
            mysql_libs.disconnect(master)

        for slv in slaves:
            print("\tSlave:  %s" % (slv.conn_msg))
            if slv.conn:
                mysql_libs.disconnect(slv)


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
    opt_val_list = ["-c", "-d", "-m", "-n", "-s", "-y"]
    opt_xor_dict = {"-M": ["-R", "-S"], "-R": ["-M", "-S"], "-S": ["-M", "-R"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):

        try:
            proglock = gen_class.ProgramLock(cmdline.argv,
                                             args_array.get("-y", ""))
            run_program(args_array, func_dict)
            del proglock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_rep_change with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
