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

