from flask import *
from flask.templating import render_template
from config import config_data
from dbConnection import *
from DataAccess import DataAccess
from ResearchGroup import ResearchGroup
from Document import *
from flask_babel import *
from flask_login import login_user, login_required
from flask_login import LoginManager
from flask_login import logout_user
from User import *
from Session import *
import sys

app = Flask(__name__, template_folder="../html/templates/", static_folder="../html/static")
app_data = {'app_name': "newName"}
app.config['BABEL_TRANSLATION_DIRECTORIES'] = "../babel/translations/"
babel = Babel(app)
connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                          dbhost=config_data['dbhost'])
app.secret_key = b'&-s\xa6\xbe\x9b(g\x8a~\xcd9\x8c)\x01]\xf5\xb8F\x1d\xb2'
login_manager = LoginManager()
login_manager.init_app(app)


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
        lang = request.accept_languages.best_match(config_data['supported_langs'])
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


@app.route("/researchgroups/")
def show_research_groups():
    '''
    Shows the research groups on the website
    :return: Rendered template containing all research groups
    '''
    access = DataAccess(connection)
    groups = access.get_researchGroups()
    return render_template("researchgroups.html", r_groups=groups, page="rgroups")


@app.route("/researchgroups/", methods=["POST"])
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


@app.route("/people/", methods=["GET"])
def show_people():
    '''
    Shows a table of people on a webpage
    :return: Rendered template of people HTML
    '''
    access = DataAccess(connection)
    researchGroups = access.get_researchGroups()

    if request.args.get("Name") is None:

        people = access.get_employees()


    else:
        researchGroupOptions = [""]

        for iter in researchGroups:
            researchGroupOptions.append(iter.name)

        name = request.args.get("Name")
        groupNr = int(request.args.get("Research_group"))
        group = researchGroupOptions[groupNr]
        promotor = int(request.args.get("Promotor"))

        people = access.filter_employees(name, group, promotor)

    neededValuesPeoplePage = []
    for person in people:
        for group in researchGroups:
            if (group.ID == person.research_group):
                neededValuesPeoplePage.append([person.name, group.name, person.promotor])

    return render_template("people.html", r_values=neededValuesPeoplePage, r_researchGroups=researchGroups,
                           page="people")



def helper_sort_values_projects(projects, researchGroups):
    neededValuesProject = []
    for project in projects:
        for group in researchGroups:
            if (group.ID == project.researchGroup):
                neededValuesProject.append([project.title, group.name, project.maxStudents])

    return neededValuesProject


@app.route("/projects/", methods=["GET"])
def show_projects():
    access = DataAccess(connection)
    projects = access.get_projects()
    researchGroups = access.get_researchGroups()

    neededValuesProject = helper_sort_values_projects(projects, researchGroups)

    return render_template("projects.html", r_values=neededValuesProject, r_researchGroups=researchGroups,
                           page="projects")\

# TODO meerdere promotors kunnen in 1 project, geeft nu enkel 1 weer
@app.route("/projects/<int:id>", methods = ['GET'])
def project_page(id):
    access = DataAccess(connection)
    project = access.get_project(id)
    document = access.get_projectDocuments(id)
    promotors = access.get_projectPromotors(id)
    emp = access.get_employee(promotors[0])

    researchGroup = access.get_researchGroupOnID(project.researchGroup)

    return render_template("project.html", r_project=project, r_document = document, r_promotor = emp,
                           r_researchGroup = researchGroup,
                           page="projects")


@app.route("/projects/search", methods=["GET"])
def apply_filter_projects():
    access = DataAccess(connection)
    researchGroups = access.get_researchGroups()


    if request.args.get("Search_query") == None:

        projects = access.get_projects()


    else:
        typeOptions = ["", "Bachelor dissertation", "Master thesis", "Research internship 1", "Research internship 2"]
        disciplineOptions = [None, ["MathematicsCompSc"], ["Mathematics"], ["Computer Science"],
                             ["MathematicsCompSc", "Mathematics"], ["MathematicsCompSc", "Computer Science"],
                             ["Mathematics", "Computer Science"], ["MathematicsCompSc", "Mathematics", "Computer Science"]]
        researchGroupOptions = [""]

        for iter in researchGroups:
            researchGroupOptions.append(iter.name)

        query = request.args.get("Search_query")
        print(query, file=sys.stderr)
        typeNr = int(request.args.get("Type"))
        type = typeOptions[typeNr]
        disciplineNr = int(request.args.get("Disciplines"))
        discipline = disciplineOptions[disciplineNr]
        groupNr = int(request.args.get("Research_group"))
        group = researchGroupOptions[groupNr]
        status = int(request.args.get("Status"))

        projects = access.filter_projects(query, type, discipline, group, status)


    neededValuesProject = helper_sort_values_projects(projects, researchGroups)
    return render_template("projects.html", r_values=neededValuesProject, r_researchGroups=researchGroups,
                           page="projects")


@app.errorhandler(404)
def handle_404(e):
    '''
    Handles error 404 (missing page)
    :param e: Exception container
    :return: Rendered template of the 404.html file
    '''
    return render_template("404.html"), 404


@app.route("/lang/", methods=["GET"])
def pick_language():
    lang = request.args.get('send')
    url = request.args.get('url_redirect')
    resp = make_response(redirect(url))
    resp.set_cookie('lang', lang)
    return resp


@login_manager.user_loader
def load_user(user_id):
    return User(Session(1, user_id, 0, 0))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    login_user(User(Session(1, 1, 0, 0)))
    flash('Logged in successfully.')
    next = request.args.get('login')
    flash("you are now logged in")
    return redirect(next or url_for('index'))


@app.route("/logout/", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    next = request.args.get('logout')
    flash("you are now logged out")
    return redirect(next or url_for('index'))


if __name__ == "__main__":
    ip = config_data['ip']
    port = config_data['port']
    access = DataAccess(connection)
    temp=access.get_researchGroupOnID(1)
    temp2=access.get_projectPromotors(1)
    app.run(debug=True, host=ip, port=port)
