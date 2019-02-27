### Project Databases
from flask import Flask
from flask.templating import render_template
from flask import request, session, jsonify

from config import config_data
from dbConnection import DBConnection

from dbAcces import *
from dbDocument import *

### INITIALIZE SINGLETON SERVICES ###
app = Flask('PROJECTDB ')
app.secret_key = '*^*(*&)(*)(*afafafaSDD47j\3yX R~X@H!jmM]Lwf/,?KT'
app_data = {}
app_data['app_name'] = "newName"##config_data['app_name']
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'] ,dbpass=config_data['dbpass'], dbhost=config_data['dbhost'])

### VIEW ###
@app.route("/")
def main():
    return


### RUN DEV SERVER ###
if __name__ == "__main__":
    # app.run()
    acces=dbAcces(connection)
    while(True):
        inp=input("geeft input")
        if (inp=="makedoc"):
            inp=input("geeft uw document")
            acces.add_document(dbDocument(inp))
        elif(inp=="getdoc"):
            temp=acces.get_Document()
            for doc in temp:
                print(doc.text)
        elif(inp=="getgroup"):
            temp=acces.get_researchGroup()
            for i in temp:
                print(i.name+" "+i.abbreviation+" "+i.discipline+" "+str(i.active)+" "+i.adress+" "+i.telNr+" "+i.groupDescription)
        elif(inp=="makegroup"):
            name=input("give name")
            abb=input("give abbreviation")
            disc=input("give discipline")
            active=input("give active")=="True"
            adress=input("give adress")
            tel=input("give number")
            desc=input("give decription")
            temp=dbResearchGroup(name,abb,disc,active,adress,tel,desc)
            acces.add_researchGroup(temp)

        elif(inp=="quit"):
            break
    
    
