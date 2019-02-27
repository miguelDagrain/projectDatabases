### Project Databases
from flask import Flask
from flask.templating import render_template
from flask import request, session, jsonify

from config import config_data
from dbConnection import DBConnection

from dbAcces import dbAcces

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
    temp=acces.get_Document()
    for doc in temp:
        print(doc.m_text)
    
    
