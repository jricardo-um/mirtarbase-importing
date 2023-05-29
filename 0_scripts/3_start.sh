#!/bin/bash
web="https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#run-mongodb-community-edition"
sudo systemctl start mongod
systemctl status mongod || echo $web