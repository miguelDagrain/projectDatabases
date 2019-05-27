# ESP 2.0 #

This project is created for the course <i>Programming project databases</i>. This repository is the remote repository of 
our ESP website and is created by Thibaut Van Goethem, Olivier Van Houtte, Miguel Dagrain, Robbe Van de Velde and Freek De Sagher.
<br>A running version of this application can be found at http://studento.uantwerpen.be:5001

### Dependencies
<p>Our project depends on some additional Python packages:</p>

* Flask
* Flask-Login
* Flask-Babel
* psycopg2

To install these dependencies, run 
> <i>pip install \<package name> </i><br>

To configure LDAP follow [these](#setting-up-ldap) steps.

### Configure and run our project

In the Backend folder there is a file called [config.py](Backend/config.py). This file contains the configuration of our
application. In this file you can configure the database (IP, username, password), the server IP and port, the login mode can be 
specified (normal: login without LDAP, ldap: login with LDAP) and the user can specify whether the tags need to be calculated
or if the application should run in Debug mode or not.

<br>

In order to create the database, follow the steps in this paragraph. The files needed for this step are found in the [sql folder](sql).
<br>First, create the database.
> psql -U _\<username\>_ -f create_database.sql

Then create all tables and relations.
> psql -U pdb -d pdbdatabase -f ESP.sql

Fill the database with the actual data from the original ESP.
> psql -U pdb -d pdbdatabase -f Data.sql

The database is now ready to use.

<br>

For the translations to work properly, the following command needs to be executed to compile the translations:
> pybabel compile -d babel/translations

Once everything is configured, go to the Backend folder and run app.py with 
> python3 app.py. 

<br>

The webapplication will run on
the IP and port specified in [config.py](Backend/config.py).

### Dummy login accounts

To demonstrate all the functionality of our web application, we created some dummy accounts for a student, an employee and
an administrator which can be used to login to our website. <br>
>**Normal users (no LDAP)**
> * student account: username: student, password: hunter3
> * employee account: username: employee, password: hunter2
> * administrator account: username: admin, password: hunter1

>**LDAP users**
> * students: username: student number, password: hunter2 <br>
> * employees and administrators: username: first + last name (ex. Chris Blondia), password: hunter1

### Flask-Babel translations

In this section you find information on how to update translation or how to add new translations.
All files regarding translation are found in the babel folder.

In order to create new Dutch translations, run the next commands from the project root.
> pybabel extract -F babel/babel.cfg -o babel/messages.pot . <br>
> pybabel update -i babel/messages.pot -d babel/translations

After this is done, go to the [messages.po](babel/translations/nl/LC_MESSAGES/messages.po) file, and fill in the new entries.

To update translations, go to the same [messages.po](babel/translations/nl/LC_MESSAGES/messages.po) file and change the entries' translation
to whatever you like.

Remember to compile the translation after you made changes with the command
> pybabel compile -d babel/translations

This creates the compiled [messages.mo](babel/translations/nl/LC_MESSAGES/messages.mo) file next to the messages.po file.

### Setting up LDAP

We only tested LDAP in our Ubuntu environment. The steps made in this section are Ubuntu-only.

To install LDAP to your computer, execute
> sudo apt install slapd ldap-utils

Next, we will need to configure our LDAP server. Run the command
> sudo dpkg-reconfigure slapd

and follow the steps trough the installation. If you need to fill in a domain name, use _pdbldap.com_.
As organisation name, pick _pdbldap_. Make sure to pick MDB.

To fill the LDAP server with accounts, go to the [ldap folder](ldapFiles) and perform the next commands
> ldapadd -x -D cn=admin,dc=pdbldap,dc=com -W -f pdbldap_data.ldif

To add test accounts, do
> ldapadd -x -D cn=admin,dc=pdbldap,dc=com -W -f pdbldapUsers.ldif

To add the actual users do
> ldapadd -x -D cn=admin,dc=pdbldap,dc=com -W -f pdbldapRealUsers.ldif

The only thing left to do is install the Python packages and its dependencies.
> sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev <br>
> sudo pip install python-ldap



