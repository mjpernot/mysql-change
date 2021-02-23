# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


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

