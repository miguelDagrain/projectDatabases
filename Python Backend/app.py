from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from config import config_data
from dbConnection import *
from DataAccess import DataAccess
from ResearchGroup import ResearchGroup
from Document import *


app = Flask(__name__, template_folder="../html/templates/", static_folder="../html/static")
app_data = {'app_name': "newName"}
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                          dbhost=config_data['dbhost'])


@app.route("/")
def index():
    return render_template("index.html", page="index")


@app.route("/image/banner")
def get_banner():
    return "../static/image/banner.png"


@app.route("/researchgroups")
def show_research_groups():
    access = DataAccess(connection)
    groups = access.get_researchGroups()
    return render_template("researchgroups.html", r_groups=groups, page="rgroups")


@app.route("/researchgroups", methods=["POST"])
def add_research_group():
    name = request.form.get("name")
    abbrev = request.form.get("abbreviation")
    discipline = request.form.get("discipline")
    active = True if request.form.get("active") == 'on' else False
    address = request.form.get("address")
    telephone = request.form.get("telephone")
    # desc = request.form.get("description")
    desc=list()
    desc.append (Document(1 ,language.NEDERLANDS,'ik ben jos het document')) #TODO : dit aanpassen zodat het nieuwe descripties kan aanemen (nu ga ik het gewoon document 1 eraan kopellen)

    discipline = "Mathematics"  #TODO : ervoor zorgen dat je hier meerdere dinges kan invullen (mischien drop down menu?)
    r = ResearchGroup(None,name,abbrev,discipline,active,address,telephone,desc)
    access = DataAccess(connection)
    access.add_researchGroup(r)
    return render_template("index.html", send=True, page="index")


@app.route("/people")
def show_people():
    return render_template("people.html", page="people")


@app.route("/projects")
def show_projects():
    access = DataAccess(connection)
    projects = access.get_projects()
    return render_template("projects.html", r_projects=projects, page="projects")


if __name__ == "__main__":
    # acces=DataAccess(connection)
    # acces.manualDataHandling()
    # temp=acces.get_projects()
    app.run(debug=True)
