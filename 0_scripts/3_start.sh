#!/bin/bash
web="https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#run-mongodb-community-edition"
sudo echo '`sudo` successful'
if sudo systemctl start mongod ; then
	systemctl status mongod
else
	echo -e "Error, please check $web" ; fi
echo '
Useful commands for `mongosh`:
 show dbs
 use <database>
 show tables
 db.<collection>.drop()
 '
 