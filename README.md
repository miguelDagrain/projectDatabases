# README #
this project is made for the course project databases

the goal of this project is to remake the current esp website that is used by professors, master students,and phd students to handle research ideas and theses

# creating the database #

for this you already need postgres installed

create database and role
> psql -U postgres -d postgres -f sql/create_database.sql

make all the tables

> psql -U pdb -d pdbdatabase -f sql/ESP.sql

optional: insert dummy_data

> psql -U pdb -d pdbdatabase -f sql/dummy_data.sql


###Flask-Babel
 If you only want the translations you only have to do the compile step
 
 Run from projectDatabases folder

Extract all translatable messages to messages.pot
>pybabel extract -F babel.cfg -o messages.pot .

Initialize file for dutch translations

>pybabel init -i messages.pot -d translations -l nl

This will create a messages.pot in translation/nl/LC_MESSAGES where you need to translate all sentences

If you have translated it copy the messages.po to babel/translations/nl/LC_MESSAGES and run the following command

Compile translations

>pybabel compile -d babel/translations

Go to source file

>cd Backend

Run the application on http://localhost:5000
>python app.py
