from flask import *
from flask.templating import render_template
from config import config_data
from dbConnection import *
from DataAccess import DataAccess
from ResearchGroup import ResearchGroup
from Document import *
from flask_babel import *

app = Flask(__name__, template_folder="../html/templates/", static_folder="../html/static")
app_data = {'app_name': "newName"}
app.config['BABEL_TRANSLATION_DIRECTORIES'] = "../babel/translations/"
babel = Babel(app)
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                          dbhost=config_data['dbhost'])
app.secret_key = b'&-s\xa6\xbe\x9b(g\x8a~\xcd9\x8c)\x01]\xf5\xb8F\x1d\xb2'


@babel.localeselector
def get_locale():
    '''
    If the language cookie is set, use its value
    Else determine the language that fits best based on the user's accept header
    :return: Language code
    '''
    lang = request.cookies.get('lang')
    if lang is not None:
        return lang
    else:
        lang = request.accept_languages.best_match(['nl', 'en'])
        return lang


@app.route("/")
def index():
    '''
    Renders the index template
    :return: Rendered index template
    '''
    resp = make_response(render_template("index.html", page="index"))
    if request.cookies.get('lang') is None:
        lang = get_locale()
        resp.set_cookie('lang', lang)
    return resp


@app.route("/researchgroups")
def show_research_groups():
    '''
    Shows the research groups on the website
    :return: Rendered template containing all research groups
    '''
    access = DataAccess(connection)
    groups = access.get_researchGroups()
    return render_template("researchgroups.html", r_groups=groups, page="rgroups")


@app.route("/researchgroups", methods=["POST"])
def add_research_group():
    '''
    Adds a research group to the database
    This function is called whenever the user uses the POST method on the
    research group page
    :return: Rendered template of the index with a send message
    '''
    name = request.form.get("name")
    abbrev = request.form.get("abbreviation")
    discipline = request.form.get("discipline")
    active = True if request.form.get("active") == 'on' else False
    address = request.form.get("address")
    telephone = request.form.get("telephone")
    # desc = request.form.get("description")
    desc = list()
    desc.append(Document(1, language.NEDERLANDS,
                         'ik ben jos het document'))  # TODO : dit aanpassen zodat het nieuwe descripties kan aanemen (nu ga ik het gewoon document 1 eraan kopellen)

    discipline = "Mathematics"  # TODO : ervoor zorgen dat je hier meerdere dinges kan invullen (mischien drop down menu?)
    r = ResearchGroup(None, name, abbrev, discipline, active, address, telephone, desc)
    access = DataAccess(connection)
    access.add_researchGroup(r)
    return render_template("index.html", send=True, page="index")


@app.route("/people")
def show_people():
    '''
    Shows a table of people on a webpage
    :return: Rendered template of people HTML
    '''
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
    '''
    Handles error 404 (missing page)
    :param e: Exception container
    :return: Rendered template of the 404.html file
    '''
    return render_template("404.html"), 404


@app.route("/lang", methods=["GET"])
def pick_language():
    lang = request.args.get('lang')
    resp = make_response(redirect('/'))
    resp.set_cookie('lang', lang)
    return resp



if __name__ == "__main__":
    # acces=DataAccess(connection)
    # acces.manualDataHandling()
    # temp=acces.get_projects()

    app.run(debug=True)
