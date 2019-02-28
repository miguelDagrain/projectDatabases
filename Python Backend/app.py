from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from config import config_data
from dbConnection import *
from DataAccess import DataAccess
from ResearchGroup import ResearchGroup

app = Flask(__name__, template_folder="../html/templates/", static_folder="../html/static")
app_data = {'app_name': "newName"}
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                          dbhost=config_data['dbhost'])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/researchgroups")
def show_research_groups():
    access = DataAccess(connection)
    groups = access.get_researchGroups()
    return render_template("researchgroups.html", r_groups=groups)


@app.route("/researchgroups", methods=["POST"])
def add_research_group():
    name = request.form.get("name")
    abbrev = request.form.get("abbreviation")
    discipline = request.form.get("discipline")
    active = True if request.form.get("active") == 'on' else False
    address = request.form.get("address")
    telephone = request.form.get("telephone")
    desc = request.form.get("description")
    desc = "wij zijn een groep" # enige mogelijkheid op de moment
    discipline = "Mathematics"  # enige mogelijkheid op de moment
    r = ResearchGroup(name,abbrev,discipline,active,address,telephone,desc)
    access = DataAccess(connection)
    access.add_researchGroup(r)
    return render_template("index.html", send=True)


if __name__ == "__main__":
    # acces=DataAccess(connection)
    # acces.manualDataHandling()
    app.run(debug=True)
