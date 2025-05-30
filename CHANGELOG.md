# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [4.0.1] - 2025-05-30
- Updated python-lib to v4.0.1
- Updated mysql-lib to v5.5.1
- Removed support for MySQL 5.6/5.7

### Changed
- Documentation changes.


## [4.0.0] - 2025-02-18
Breaking Changes

- Removed support for Python 2.7.
- Updated mysql-lib v5.4.0
- Updated python-lib v4.0.0

### Changed
- Converted strings to f-strings.
- Documentation changes.

### Deprecated
- Support for MySQL 5.6/5.7


## [3.2.5] - 2024-11-19
- Updated python-lib to v3.0.8
- Updated mysql-lib to v5.3.9

### Fixed
- Set chardet==3.0.4 for Python 3.


## [3.2.4] - 2024-11-11
- Updated chardet==4.0.0 for Python 3
- Updated distro==1.9.0 for Python 3
- Updated protobuf==3.19.6 for Python 3
- Updated mysql-connector-python==8.0.28 for Python 3
- Updated mysql-lib to v5.3.8
- Updated python-lib to v3.0.7
        
### Deprecated
- Support for Python 2.7
        

## [3.2.3] - 2024-09-27
- Updated simplejson==3.13.2 for Python 3
- Updated python-lib to v3.0.5
- Updated mysql-lib to v5.3.7


## [3.2.2] - 2024-09-10

### Changed
- config/mysql_cfg.py.TEMPLATE:  Changed cfg_file default value.
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.


## [3.2.1] - 2024-02-29
- Updated to work in Red Hat 8
- Updated python-lib to v3.0.3
- Updated mysql-lib to v5.3.4

### Changed
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [3.2.0] - 2023-08-23
- Upgraded python-lib to v2.10.1
- Replaced the arg_parser code with gen_class.ArgParser code.

### Changed
- Multiple functions: Replaced the arg_parser code with gen_class.ArgParser code.
- main: Removed gen_libs.get_inst call.


## [3.1.2] - 2022-11-22
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded mysql-lib to v5.3.2

### Changed
- Converted imports to use Python 2.7 or Python 3.


## [3.1.1] - 2022-06-27
- Upgraded python-lib to v2.9.2
- Upgraded mysql-lib to v5.3.1
- Added TLS capability

### Changed
- config/mysql_cfg.py.TEMPLATE: Added TLS entry.
- config/slave.txt.TEMPLATE: Added TLS entry.
- Documentation updates.


## [3.1.0] - 2021-08-20
- Updated to work in MySQL 8.0 and 5.7 environments.
- Updated to work in a SSL environment.
- Updated to use the mysql_libs v5.2.2 library.
- Updated to use gen_libs v2.8.4 library.

### Changed
- create_instances:  Receive slv_key argument and call gen_libs.transpose_dict function and changed cmds_gen to gen_libs.
- run_program:  Add \*\*kwargs to parameter list and pass to create_instances call.
- main:  Setup slv_key dictionary.
- config/slave.txt.TEMPLATE:  Added SSL confioguration options.
- config/mysql_cfg.py.TEMPLATE:  Added SSL configuration options.

### Fixed
- config/mysql.cfg.TEMPLATE:  Pointed to correct socket file.

### Removed
- cmds_gen module.


## [3.0.3] - 2020-11-18
- Updated to use the mysql_libs v5.0.0 library.

### Fixed
- move_slave:  Fixed the problem where the slave now uses the replication user information from the configuration file.
- mv_slv_to_new_mst:  Does not start slaves if sync fails on a database.
- run_program:  Check for connection status of master and slaves before processing begins.
- move_slave:  Set new MasterRep's instance rep user information to that of the existing MasterRep's instance.  Temporary fix until SlaveRep allows for rep user information.
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.

### Changed
- move_slave_up, move_slave:  Refactored function to remove multiple "return" commands.
- create_instances, move_slave_up, crt_slv_mst:  Added silent option to connect method.
- move_slave, move_slave_up, run_program:  Replaced cmds_gen.disconnect call with mysql_libs.disconnect call.
- move_slave_up, move_slave:  Replaced fetch_slv call with mysql_libs.fetch_slv call.
- crt_slv_mst:  Added master connection status checks.
- move_slave_up:  Added new master and slave master connection status checks.
- run_program:  Refactored check on master and slave connection status checks.
- Removed unneccessary \*\*kwargs from arguments lists.
- move_slave_up:  Added replication user to SlaveRep instance call.
- crt_slv_mst:  Added replication user to MasteRep instance call.
- move_slave_up:  Replaced mysql_libs.create_instance with gen_libs.load_module and mysql_class.MasterRep instance call.
- create_instances:  Replaced mysql_libs.create_instance with gen_libs.load_module and mysql_class.MasterRep instance call.
- move_slave_up:  Changed arguments from positional to keywords for SlaveRep instance call.
- crt_slv_mst:  Changed arguments from positional to keywords for MasterRep instance call.
- config/mysql_cfg.py.TEMPLATE:  Changed entry to work with mysql_libs v5.0.0 library.
- config/slave.txt.TEMPLATE:  Added rep_user and rep_japd entries to configuration file.
- config/mysql_cfg.py.TEMPLATE:  Added rep_user and rep_japd entries to configuration file.
- Documentation updates.

### Removed
- fetch_slv function


## [3.0.2] - 2020-04-24
### Added
- Added ProgramLock class to prevent multiple runs at the same time.

### Fixed
- move_slave_up:  Fixed disconnect from new master and slave/master.
- fetch_slv, crt_slv_mst, mv_slv_to_new_mst, move_slave, move_slave_up, create_instances, run_program:  Fixed problem with mutable default arguments issue.
- crt_slv_mst:  Fixed naming conflict between arguments.
- move_slave_up:  Setup connect to new master connection and to new slave master connection.
- crt_slv_mst:  Setup connect to new master connection.
- create_instances:  Setup connect to master connection.
- mv_slv_to_new_mst:  Fixed naming conflict between arguments.
- main:  Fixed handling command line arguments from SonarQube scan finding.
- fetch_slv:  Fixed incorrect reference to slave name variable.

### Changed
- run_program:  Replaced "for" and "if" statements with an intersect loop to call functions.
- main:  Added ProgramLock class to implement program locking.
- config/slave.txt.TEMPLATE:  Changed format of file.
- main:  Refactored the "if" statements to streamline the checks.
- run_program, create_instances, move_slave_up, move_slave, mv_slv_to_new_mst, crt_slv_mst, fetch_slv, is_slv_up:  Changed variables to standard naming convention.
- Documentation updates.

### Removed
- Removed unused library modules.


## [3.0.1] - 2018-12-06
### Changed
- Documentation updates.


## [3.0.0] - 2018-05-23
Breaking Change

### Changed
- mysql_class, mysql_libs, cmds_gen, gen_libs, arg_parser: Changed calls to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [2.2.0] - 2018-05-03
### Changed
- Changed "server" to "mysql_class" module reference.
- Changed "commands" to "mysql_libs" module reference.

### Added
- Added single-source version control.


## [2.1.0] - 2017-08-21
### Changed
- Convert program to use local libraries from ./lib directory.
- Change single quotes to double quotes.
- Help_Message: Replace docstring with printing the programs \_\_doc\_\_.


## [2.0.0] - 2016-11-18
### Added
- Move_Slave_Up function.
- Move_Slave function.
- Is_Slv_Up function.
- Mv_Slv_2_New_Mst function.
- Crt_Slv_Mst function.
- Fetch_Slv function.

### Changed
- Major upgrade to the program to include new options such as moving a slave to under a slave/master, moving a slave to under a slave/master and removing the replication connection between the current master and the new master, and moving a slave under a slave/master to the master of the slave/master.
- main:  Added new variables and modified existing ones and added additional checks on the argument processing.
- Run_Program:  Replaced function call with code to execute functions and process error flag and messages.
- Create_Instances:  Replaced master instance creation with function call and removed check on slave setting as its a required argument.

### Deprecated
- Create_New_Mst function.
- Chg_Master function.


## [1.2.0] - 2016-09-21
### Changed
- main:  Changed options to be inline with the other programs.  Swapped -n and -M around as -M is the main function.  Replaced Arg_Parse with Arg_Parse2 function call.  Reorganized the 'if' statements to streamline the argument processing procedures.
- Chg_Master:  Changed -c to -n.
- Create_Instances:  Changed commands.Create_Cfg_Array to cmds_gen.Create_Cfg_Array.  Added config path to the argument call.
- Chg_Master:  Changed commands.Disconnect to cmds_gen.Disconnect.


## [1.1.0] - 2015-12-03
### Changed
- Chg_Master:  Added check for status of slave after change.


## [1.0.0] - 2015-12-01
- Initial creation.

