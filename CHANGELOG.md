# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.0.2] - 2020-04-24
### Fixed
- crt_slv_mst:  Fixed naming conflict between arguments.
- move_slave_up:  Setup connect to new master connection and to new slave master connection.
- crt_slv_mst:  Setup connect to new master connection.
- create_instances:  Setup connect to master connection.
- mv_slv_to_new_mst:  Fixed naming conflict between arguments.
- main:  Fixed handling command line arguments from SonarQube scan finding.
- fetch_slv:  Fixed incorrect reference to slave name variable.

### Changed
- config/slave.txt.TEMPLATE:  Changed format of file.
- main:  Refactored the "if" statements to streamline the checks.
- run_program:  Changed variables to standard naming convention.
- create_instances:  Changed variables to standard naming convention.
- move_slave_up:  Changed variables to standard naming convention.
- move_slave:  Changed variables to standard naming convention.
- mv_slv_to_new_mst:  Changed variables to standard naming convention.
- crt_slv_mst:  Changed variables to standard naming convention.
- fetch_slv:  Changed variables to standard naming convention.
- is_slv_up:  Changed variables to standard naming convention.
- Documentation updates.


## [3.0.1] - 2018-12-06
### Changed
- Documentation updates.


## [3.0.0] - 2018-05-23
Breaking Change

### Changed
- Changed "mysql_class" calls to new naming schema.
- Changed "mysql_libs" calls to new naming schema.
- Changed "cmds_gen" calls to new naming schema.
- Changed "gen_libs" calls to new naming schema.
- Changed "arg_parser" calls to new naming schema.
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

