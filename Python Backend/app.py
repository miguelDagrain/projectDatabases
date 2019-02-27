from flask import Flask
from flask.templating import render_template
from config import config_data
from dbConnection import *
from DataAccess import DataAccess

app = Flask(__name__, template_folder="../templates/")
app_data = {'app_name': "newName"}
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                          dbhost=config_data['dbhost'])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/researchgroups")
def show_research_groups():
    access = DataAccess(connection)
    groups = access.get_researchGroup()
    return render_template("researchgroups.html", r_groups=groups)


if __name__ == "__main__":
    # acces=DataAccess(connection)
    # acces.manualDataHandling()
    app.run(debug=True)
