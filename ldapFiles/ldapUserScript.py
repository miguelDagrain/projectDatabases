import dbConnection
from DataAccess import *
from Document import *
from Project import Project
from Employee import Employee
from ResearchGroup import ResearchGroup
from Session import *
from User import *
from TagCalculator import findTags
from MailService import MailService
from config import config_data

from DataAccess.employeeAccess import EmployeeAccess
from DataAccess.studentAccess import StudentAccess

dbConnection.setConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                              dbhost=config_data['dbhost'])
ldapUsers= open("pdbldapRealUsers.ldif","w+")
counter=1
eacces=EmployeeAccess()
eacces.dbconnect=dbConnection.connection
employees=eacces.get_employees()
for i in employees:
    ldapUsers.write("dn: cn="+i.name+",ou=People,dc=pdbldap,dc=com \n"
                    "objectClass: inetOrgPerson \n"
                    "objectClass: posixAccount \n"
                    "objectClass: shadowAccount \n"
                    "uid:"+i.name+"\n"
                    "sn: LASTNAME \n"
                    "givenName: FIRSTNAME \n"
                    "cn:"+i.name+" \n"
                    "displayName: DISPLAYNAME \n"
                    "uidNumber:"+str(counter)+" \n"
                    "gidNumber: 5000 \n"
                    "userPassword: hunter1 \n"
                    "gecos: FULLNAME \n"
                    "loginShell: /bin/bash \n"
                    "homeDirectory: USERDIRECTORY \n\n")
    counter+=1

sacces=StudentAccess()
sacces.dbconnect=dbConnection.connection
students=sacces.get_students()
for i in students:
    number=str(i.studentNumber)[1:]
    number="S"+number

    ldapUsers.write("dn: cn="+number+",ou=People,dc=pdbldap,dc=com \n"
                    "objectClass: inetOrgPerson \n"
                    "objectClass: posixAccount \n"
                    "objectClass: shadowAccount \n"
                    "uid:" + number + " \n"
                    "sn: LASTNAME \n"
                    "givenName: FIRSTNAME \n"
                    "cn:"+number+" \n"
                    "displayName: DISPLAYNAME \n"
                    "uidNumber:"+str(counter)+"\n"
                    "gidNumber: 5000 \n"
                    "userPassword: hunter2 \n"
                    "gecos: FULLNAME \n"
                    "loginShell: /bin/bash \n"
                    "homeDirectory: USERDIRECTORY \n\n")
    counter+=1