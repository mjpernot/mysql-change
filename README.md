# Python project for modifying a replication set in a MySQL replication schema.
# Classification (U)

# Description:
  This program is used to administrate changes in a replication set in a MySQL replication schema to include promoting a slave to master status, moving a slave to under a new master, and making a slave a master/slave.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Move slave in a slave array to under another slave in the same slave array.
  * Move slave in a slave array to under another slave in the same slave array and remove the replication connection between the current master and new master.
  * Take a slave that is under a slave/master and move it to under the master that is hosting the slave/master.


# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
    - lib/machine
    - mysql_lib/mysql_libs
    - mysql_lib/mysql_class


# Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-change.git
```

Install/upgrade system modules.

```
cd mysql-change
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:
  * Replace **{Python_Project}** with the baseline path of the python program.

Create MySQL configuration file.

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "SERVER_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "{Python_Project}/config/mysql.cfg"

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL definition file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Create a MySQL slave configuration file.

```
cp slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Program Descriptions:
### Program: mysql_rep_change.py
##### Description: Administration program for the MySQL binary log system.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-change/mysql_rep_change.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:  mysql_rep_change.py

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
        Database configuration file format (mysql_cfg.py):
            # Configuration file for {Database Name/Server}
            user = "root"
            passwd = "ROOT_PASSWORD"
            host = "IP_ADDRESS"
            serv_os = "Linux" or "Solaris"
            name = "HOSTNAME"
            port = PORT_NUMBER (default of mysql is 3306)
            cfg_file = "DIRECTORY_PATH/myisql.cfg"
            sid = "SERVER_ID"
            extra_def_file = "DIRECTORY_PATH/myextra.cfg"

            NOTE 1:  Include the cfg_file even if running remotely as the
                file will be used in future releases.

            NOTE 2:  In MySQL 5.6 - it now gives warning if password is
                passed on the command line.  To suppress this warning, will
                require the use of the --defaults-extra-file option
                (i.e. extra_def_file) in the database configuration file.
                See below for the defaults-extra-file format.

            configuration modules -> name is runtime dependent as it can be
                used to connect to different databases with different names.

            Defaults Extra File format (mysql.cfg):
            [client]
            password="ROOT_PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

            NOTE:  The socket information can be obtained from the my.cnf
                file under ~/mysql directory.

    Example:
        mysql_rep_change.py -c master -d config -s slaves.txt -M
            -m new_master_name -n slave_name


# Testing:


# Unit Testing:

### Description: Testing consists of unit testing for the functions in the mysql_rep_change.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-change.git
```

Install/upgrade system modules.

```
cd mysql-change
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Unit test runs for mysql_rep_change.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-change
```


### Unit:  help_message
```
test/unit/mysql_rep_change/help_message.py
```

### Unit:  
```
test/unit/mysql_rep_change/
```

### Unit:  
```
test/unit/mysql_rep_change/
```

### Unit:  run_program
```
test/unit/mysql_rep_change/run_program.py
```

### Unit:  main
```
test/unit/mysql_rep_change/main.py
```

### All unit testing
```
test/unit/mysql_rep_change/unit_test_run.sh
```

### Code coverage program
```
test/unit/mysql_rep_change/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the mysql_rep_change.py program.

### Installation:

Install the project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-change.git
```

Install/upgrade system modules.

```
cd mysql-change
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd test/integration/mysql_rep_change/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup.
    - passwd = "ROOT_PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - sid = SERVER_ID
    - extra_def_file = '{Python_Project}/config/mysql.cfg'

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Create a MySQL slave configuration file.

```
cp ../../../../config/slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Integration test runs for mysql_rep_change.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-change
```

### Integration:  
```
test/integration/mysql_rep_change/
```

### All integration testing
```
test/integration/mysql_rep_change/integration_test_run.sh
```

### Code coverage program
```
test/integration/mysql_rep_change/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the mysql_rep_change.py program.

### Installation:
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

Install the project using git.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-change.git
```

Install/upgrade system modules.

```
cd mysql-change
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create MySQL configuration file.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd test/blackbox/mysql_rep_change/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - sid = SERVER_ID
    - extra_def_file = '{Python_Project}/config/mysql.cfg'

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Create a MySQL slave configuration file.

```
cp ../../../../config/slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Blackbox test run for mysql_rep_change.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-change
```

### Blackbox:  
```
test/blackbox/mysql_rep_change/blackbox_test.sh
```

