# ejabberd-web-registration
Simple Jabber registration using Python 3

The webserver has to run with the ejabberd user in order to be able to use the ejabberdctl program which performs registration.
In order to do so, the sudo command will be used.

Your ejabberd installation has to use a MySQL database to run this program. (Can also be a MySQL-compatible DBMS such as MariaDB)

## Dependencies
First install the MySQL connector (MariaDB fork in this case). This is a debian installation using apt, but you can install the appropriate package depending on your distribution.
`sudo apt install python3-mysqldb libmariadbclient-dev #libmysqlclient-dev package for standard MySQL database`
Python3 will need a few libraries to run this code
`sudo -H -u ejabberd pip3 install flask`
`sudo -H -u ejabberd pip3 install flask_recaptcha`
`sudo -H -u ejabberd pip3 install flask-mysqldb`

## Running
This is as simple as :
`sudo -H -u ejabberd python3 index.py`
You can also run it in background like this :
`coming soon`
