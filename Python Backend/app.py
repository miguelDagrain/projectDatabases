from flask import Flask, request, redirect, url_for, session
from flask.templating import render_template
from config import config_data
from dbConnection import *
from DataAccess import DataAccess
from ResearchGroup import ResearchGroup
from Document import *
from flask_babel import *

app = Flask(__name__, template_folder="../html/templates/", static_folder="../html/static")
app_data = {'app_name': "newName"}
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                          dbhost=config_data['dbhost'])
app.secret_key = b'&-s\xa6\xbe\x9b(g\x8a~\xcd9\x8c)\x01]\xf5\xb8F\x1d\xb2'


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
    access = DataAccess(connection)
    people = access.get_employees()
    researchGroups = access.get_researchGroups()

    neededValuesPeoplePage = []
    for person in people:
        for group in researchGroups:
            if (group.ID == person.research_group):
                neededValuesPeoplePage.append([person.name, group.name])

    return render_template("people.html", r_values=neededValuesPeoplePage, page="people")


def helper_sort_values_projects(projects, researchGroups):
    neededValuesProject = []
    for project in projects:
        for group in researchGroups:
            if (group.ID == project.researchGroup):
                neededValuesProject.append([project.title, group.name, project.maxStudents])

    return neededValuesProject


@app.route("/projects")
def show_projects():
    access = DataAccess(connection)
    projects = access.get_projects()
    researchGroups = access.get_researchGroups()

    neededValuesProject = helper_sort_values_projects(projects, researchGroups)

    return render_template("projects.html", r_values=neededValuesProject, page="projects")


@app.route("/projects", methods=["POST"])
def apply_filter_projects():
    access = DataAccess(connection)
    query = request.form.get("Search_query")
    type = request.form.get("Type")
    discipline = request.form.get("Disciplines")
    group = request.form.get("Research_group")
    status = request.form.get("Status")

    projects = access.filter_projects(query, type, discipline, group, status)
    researchGroups = access.get_researchGroups()

    neededValuesProject = helper_sort_values_projects(projects, researchGroups)

    return render_template("projects.html", r_values=neededValuesProject, page="projects")


@app.errorhandler(404)
def handle_404(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # acces=DataAccess(connection)
    # acces.manualDataHandling()
    # temp=acces.get_projects()
    app.run(debug=True)
