import json
import re
import sys
import datetime
from functools import wraps

from flask import *
from flask.templating import render_template
from flask_babel import *
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user

import dbConnection
from DataAccess import *
from Document import *
from Project import Project
from Employee import Employee
from ResearchGroup import ResearchGroup
from Session import *
from User import *
from MailService import MailService
from config import config_data

from helperFunc import *

app = Flask(__name__, template_folder="../html/templates/", static_folder="../html/static")
app_data = {'app_name': "newName"}
app.config['BABEL_TRANSLATION_DIRECTORIES'] = "../babel/translations/"
babel = Babel(app)
app.secret_key = b'&-s\xa6\xbe\x9b(g\x8a~\xcd9\x8c)\x01]\xf5\xb8F\x1d\xb2'
login_manager = LoginManager()
login_manager.init_app(app)


# overriding the login manager of flask login to support roles, inspired from 
# https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes 
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            temp = current_user
            if not current_user.is_authenticated():
                return login_manager.unauthorized()
            if ((role not in current_user.roles) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@babel.localeselector
def get_locale():
    """
    If the language cookie is set, use its value
    Else determine the language that fits best based on the user's accept header
    :return: Language code
    """
    lang = request.cookies.get('lang')
    if lang is not None:
        return lang
    else:
        lang = request.accept_languages.best_match(config_data['supported_langs'])
        return lang


@app.route("/")
def index():
    """
    Renders the index template
    :return: Rendered index template
    """
    resp = make_response(render_template("home.html", page="index", homedoc="<h1>Todo:</h1><div>Tinymce doet moeilk.</div><div>Lelijke errors van missing file.</div><div>Waar haal k die file vandaan??</div><div>Check console voor meer info.</div>"))
    if request.cookies.get('lang') is None:
        lang = get_locale()
        resp.set_cookie('lang', lang)
    return resp


@app.route("/researchgroups/")
def show_research_groups():
    """
    Shows the research groups on the website
    :return: Rendered template containing all research groups
    """
    access = ResearchGroupAccess()
    groups = access.get_researchGroups()
    access = DomainAccess()
    disciplines = access.get_disciplines()
    return render_template("researchgroups.html", r_groups=groups, r_disciplines=disciplines, page="rgroups")


@app.route("/researchgroups/", methods=["POST"])
def add_research_group():
    """
    Adds a research group to the database
    This function is called whenever the user uses the POST method on the
    add research group page
    :return: Rendered template of the administration-add-group with disciplines and a send message
    """
    if request.form.get("Name") is None:
        return show_research_groups()

    Daccess = DomainAccess()
    disciplines = Daccess.get_disciplines()

    name = request.form.get("Name")
    abbrev = request.form.get("Abbreviation")
    disciplineNr = request.form.get("Discipline")
    discipline = disciplines[int(disciplineNr)]
    active = True #active wordt gebruikt voor leesbaarheid
    address = request.form.get("Address")
    telephone = request.form.get("Telephone")
    # desc = request.form.get("Description")
    desc = list()
    desc.append(Document(1, 'dutch',
                         'ik ben jos het document'))  # TODO : dit aanpassen zodat het nieuwe descripties kan aanemen (nu ga ik het gewoon document 1 eraan kopellen)

    r = ResearchGroup(None, name, abbrev, discipline, active, address, telephone, desc)
    Raccess = ResearchGroupAccess()
    Raccess.add_researchGroup(r)
    researchGroups = Raccess.get_researchGroups()
    return render_template("researchgroups.html", r_groups=researchGroups, r_disciplines=disciplines, page="rgroups")


@app.route("/researchgroups/<int:id>", methods=["GET"])
def group_page(id):
    """
    Renders a template with the description of a project
    :param id: the id of the researchgroup
    :return: rendered template of the group
    """
    Racces = ResearchGroupAccess()
    researchGroup = Racces.get_researchGroupOnID(id)

    Eacces = EmployeeAccess()
    researchers = list()
    contactPersons = list()
    for empl in Eacces.get_employees():
        if empl.research_group == researchGroup.ID:
            researchers.append(empl)
        if empl.id == researchGroup.contactID:
            contactPersons.append(empl)

    Pacces = ProjectAccess()
    projects = list()
    for project in Pacces.get_projects():
        if project.researchGroup[0] == researchGroup.ID:
            projects.append(project)

    language = request.cookies.get('lang')
    description = None
    for doc in researchGroup.desc:
        if doc.language == language:
            description = doc.text

    return render_template("researchgroup.html", r_groupName=researchGroup.name, r_groupID=researchGroup.ID,
                           r_description=description, r_researchers=researchers, r_contactPersons=contactPersons,
                           r_projects=projects)


@app.route("/researchgroups/<int:id>", methods=["POST"])
def apply_remove_group(id):
    """
    function that removes a research group and redirects to the researchgroups page
    :param id: id of the group to be removed
    :return: redirection to researchgroups page
    """

    Racces = ResearchGroupAccess()
    Racces.remove_researchGroup(id)

    return redirect(url_for('show_research_groups'))


@app.route("/people/", methods=["GET"])
def show_people():
    """
    Shows a table of people on a webpage
    :return: Rendered template of people HTML
    """
    Raccess = ResearchGroupAccess()
    researchGroups = Raccess.get_researchGroups()

    if request.args.get("Name") is None:
        Eaccess = EmployeeAccess()
        people = Eaccess.get_employees()


    else:
        researchGroupOptions = [""]

        for iter in researchGroups:
            researchGroupOptions.append(iter.name)

        name = request.args.get("Name")
        groupNr = int(request.args.get("Research_group"))
        group = researchGroupOptions[groupNr]
        promotor = int(request.args.get("Promotor"))

        people = Raccess.filter_employees(name, group, promotor)

    neededValuesPeoplePage = []
    for person in people:
        for group in researchGroups:
            if group.ID == person.research_group:
                neededValuesPeoplePage.append([person.name, group.name, person.promotor, person.id])

    return render_template("people.html", r_values=neededValuesPeoplePage, r_researchGroups=researchGroups,
                           page="people")


@app.route("/people/", methods=["POST"])
def add_staff():
    """
    function that adds a staff member to the database, is called everytime the user uses the POST method on the
    add staf form of the people page
    :return: redirection to show people
    """
    Raccess = ResearchGroupAccess()
    researchGroups = Raccess.get_researchGroups()

    Daccess = DomainAccess()
    name = request.form.get("Name")
    email = request.form.get("Email")
    office = request.form.get("Office")
    researchgroupNr = request.form.get("Researchgroup")
    research_group = researchGroups[int(researchgroupNr)]
    titleOptions = Daccess.get_titles()
    titleNr = request.form.get("Title")
    title = titleOptions[int(titleNr)]
    roleOptions = Daccess.get_intextOrigin()
    roleNr = request.form.get("Role")
    role = roleOptions[int(roleNr)]
    active = True #active wordt gebruikt voor leesbaarheid
    promotor = True if request.form.get("Promotor") == 'on' else False

    emp = Employee(None, name, email, office, research_group, title, role, active, promotor)
    Eaccess = EmployeeAccess()
    Eaccess.add_employee(emp)
    return redirect(url_for('show_people'))


@app.route("/people/<int:id>", methods=["GET"])
def get_person(id):
    """
    function that return a tab of the person whose id agrees with the given id
    :param id: id of the person whose tab we like to visit
    :return: rendered template of person.html with the person as attribute
    """
    Eaccess = EmployeeAccess()
    person = Eaccess.get_employee(id)

    Raccess = ResearchGroupAccess()
    group = Raccess.get_researchGroupOnID(person.research_group)

    projects = person.getProjects()

    yearAndProject = dict()

    for project in projects:
        for year in project.activeYear:
            if(year in yearAndProject):
                yearAndProject[year].append(project)
            else:
                yearAndProject[year] = list()
                yearAndProject[year].append(project)

    orderedYearAndProject = sorted(yearAndProject.items(), key= lambda k : k[0], reverse=True)

    return render_template("person.html", r_person=person, r_groupName=group.name,
                           r_projectAndYear=orderedYearAndProject, page="people")


@app.route("/people/<int:id>", methods=["POST"])
def apply_remove_person(id):
    """
    function that removes the person on whose id agrees with the given id
    :param id: id of the person to be removed
    :return: redirection to show_people
    """
    Eaccess = EmployeeAccess()
    Eaccess.remove_employee(id)

    return redirect(url_for('show_people'))


@app.route("/projects/", methods=["GET"])
def show_projects():
    access = FullDataAccess()
    projects = access.get_project_filter_data()
    researchGroups = access.get_researchGroups()
    disciplines = access.get_disciplines()
    types = access.get_projectType()
    projData = {}
    words = {}

    for proj in projects:
        researchGroupNames = []
        for rg in proj.researchGroup:
            researchGroupNames.append(access.get_researchGroupsOnIDs(rg)[0].name)

        typeNames = []
        for tp in proj.type:
            typeNames.append(tp[0])

        disciplineNames = []
        for dc in proj.discipline:
            disciplineNames.append(dc[0])

        pjson = {"ID": proj.ID, "title": proj.title, "status": proj.active, "type": typeNames, "tag": proj.tag,
                 "discipline": disciplineNames , "researchGroup": researchGroupNames, "maxStudents": proj.maxStudents,
                 "registeredStudents": proj.registeredStudents}
        for d in proj.desc:
            textstr = d.text
            rgx = re.compile("(\w[\w']*\w|\w)")
            list = rgx.findall(textstr)
            for w in list:
                if not w in words:
                    words[w] = {}
                    words[w]["total"] = 0

                if str(proj.ID) in words[w]:
                    words[w][str(proj.ID)] +=1
                    words[w]["total"] +=1
                else:
                    words[w][str(proj.ID)] =1
                    words[w]["total"] +=1

        projData[proj.ID] = pjson

    return render_template("projects.html", r_projects=projects, r_researchGroups=researchGroups,
                           r_disciplines=disciplines, r_types=types, page="projects",
                           alt=json.dumps(projData, default=lambda x: x.__dict__), words=json.dumps(words, default=lambda x: x.__dict__))


@app.route("/projects/", methods=["POST"])
def add_project():

    access = FullDataAccess()

    title = request.json["Title"]


    maxStudents = request.json["Maxstudents"]

    project = Project(None, title, maxStudents, True)


    researchGroupNrs = request.json["Researchgroup"]

    for researchGroupNr in researchGroupNrs:
        project.researchGroup.append(int(researchGroupNr))


    #todo: aanpassen zodat documenten in andere talen kunnen worden toegevoegd
    descriptionText = request.json["Description"]

    project.desc.append(Document(None, "dutch", descriptionText))


    typeNrs = request.json["Type"]
    typeOptions = access.get_projectType()

    for typeNr in typeNrs:
        project.type.append(typeOptions[int(typeNr)])

    disciplineNrs = request.json["Discipline"]

    for disciplineNr in disciplineNrs:
        project.discipline.append(int(disciplineNr))


    #todo: toevoegen zodat er onderscheid is tussen promotors en begeleiders
    promotorsNameArray = request.json["Promotors"]

    promotorOptions = access.get_employees()
    promotorNameId = {promotorOption.name:promotorOption.id for promotorOption in promotorOptions}

    for promotorName in promotorsNameArray:
        if promotorName in promotorNameId: #dit zal normaal gezien true geven voor alle mogelijke inputs omdat javascript hierop al controleerde
            project.promotor.append(promotorNameId[promotorName])


    tags = request.json["Tags"]
    project.tag = list(tags)


    related = request.json["Related"]

    relatedProjectOptions = access.get_projects()
    relatedProjectTitleId = {relatedProjectOption.title:relatedProjectOption.ID for relatedProjectOption in relatedProjectOptions}

    for relatedProjectTitle in related:
        if relatedProjectTitle in relatedProjectTitleId:
            project.relatedProject.append(relatedProjectTitleId[relatedProjectTitle])

    now = datetime.now()
    project.activeYear.append(now.year)

    access.add_project(project)

    return jsonify(result=True)

    

# TODO meerdere promotors kunnen in 1 project, geeft nu enkel 1 weer
@app.route("/projects/<int:id>", methods=['GET'])
def project_page(id):
    Paccess = ProjectAccess()
    Eaccess = EmployeeAccess()
    Raccess = ResearchGroupAccess()
    project = Paccess.get_project(id)
    document = Paccess.get_projectDocuments(id)
    promotorsIDs = Paccess.get_projectPromotors(id)
    promotors = list()
    for promotorID in promotorsIDs:
        promotors.append(Eaccess.get_employee(promotorID))

    researchGroups = Raccess.get_researchGroupsOnIDs(project.researchGroup)


    return render_template("project.html", r_project=project, r_promotors=promotors,
                           r_researchGroups=researchGroups, page="projects")


@app.route("/projects/<int:id>", methods=["POST"])
def apply_remove_project(id):
    Paccess = ProjectAccess()
    Paccess.remove_project(id)

    return redirect(url_for('show_projects'))


@app.route("/projects/search", methods=["GET"])
def apply_filter_projects():
    if request.args.get("Search_query") is None:
        return show_projects()
    else:
        Raccess = ResearchGroupAccess()
        researchGroups = Raccess.get_researchGroups()
        typeOptions = ["", "Bachelor dissertation", "Master thesis", "Research internship 1", "Research internship 2"]
        Daccess = DomainAccess()
        disciplineOptions = Daccess.get_disciplines()
        researchGroupOptions = [""]

        for iter in researchGroups:
            researchGroupOptions.append(iter.name)

        query = request.args.get("Search_query")
        print(query, file=sys.stderr)
        typeNr = int(request.args.get("Type"))
        type = typeOptions[typeNr]

        disciplineNrs = request.args.getlist("Disciplines")
        discipline = helper_get_selected_multi_choice(disciplineNrs, disciplineOptions)

        groupNr = int(request.args.get("Research_group"))
        group = researchGroupOptions[groupNr]
        status = int(request.args.get("Status"))

        Paccess = ProjectAccess()
        projects = Paccess.filter_projects(query, type, discipline, group, status)

        return render_template("projects.html", r_projects=projects, r_researchGroups=researchGroups,
                               r_disciplines=disciplineOptions, r_types=typeOptions, page="projects",
                               alt=json.dumps(projects, default=lambda x: x.__dict__))


@app.route("/administration/")
@login_required(role='admin')
def get_administration():
    return render_template("administration.html", page="administration")


@app.route("/administration/modify_disciplines", methods=["GET"])
def form_modify_disciplines():
    """
    function that returns a form to modify disciplines
    :return: Rendered template of the administration-modify-disciplines with disciplines
    """
    access = DomainAccess()
    disciplines = access.get_disciplines()

    return render_template("administration-modify-disciplines.html", r_disciplines=disciplines, send=False)


@app.route("/administration/modify_disciplines", methods=["POST"])
def modify_disciplines():
    """
    function that adds a discipline to the possible disciplines
    :return: Rendered template of the administration-modify-disciplines with disciplines
    """
    access = DomainAccess()
    disciplines = access.get_disciplines()

    value = request.form.get("Name")
    if value:
        access.add_discipline(value)
    else:
        value = request.form.get("Discipline")
        if value:
            discipline = disciplines[int(value)]
            access.remove_discipline(discipline)

    disciplines = access.get_disciplines()

    return render_template("administration-modify-disciplines.html", r_disciplines=disciplines, send=True)


@app.route("/administration/modify_types", methods=["GET"])
def form_modify_types():
    """
    function that returns a form to modify types
    :return: Rendered template of the administration-modify-templates with types
    """
    access = FullDataAccess
    types = access

    return render_template("administration-modify-types.html", r_types=types, send=False)


@app.route("/administration/modify_types", methods=["POST"])
def modify_types():
    """
    function that modifies
    :return:
    """


# @app.errorhandler(404)
# def handle_404(e):
#     '''
#     Handles error 404 (missing page)
#     :param e: Exception container
#     :return: Rendered template of the 404.html file
#     '''
#     return render_template("404.html"), 404


@app.route("/lang/", methods=["GET"])
def pick_language():
    lang = request.args.get('send')
    url = request.args.get('url_redirect')
    resp = make_response(redirect(url))
    resp.set_cookie('lang', lang)
    return resp


# alles onder de check is om vragen uit javascript te beantwoorden met json (gegevens uit de database), het
# is niet de bedoeling dat een je deze url gebruikt vanuit de website, dan zullen ze doorsturen naar de home page
@app.route("/check/empl_names", methods=["GET"])
def check_empl_names():
    Eaccess = EmployeeAccess()
    employees = Eaccess.get_employees()

    given_letters = request.args.get("letters")

    possibilities = list()

    for empl in employees:
        if given_letters in empl.name:
            possibilities.append(empl.name)
            if len(possibilities) > 4:
                break

    return jsonify(possibilities)


@app.route("/check/empl_name_correct", methods=["GET"])
def check_empl_name_correct():
    Eaccess = EmployeeAccess()
    employees = Eaccess.get_employees()

    given_name = request.args.get('input')

    for empl in employees:
        if given_name == empl.name:
            return jsonify(True)

    return jsonify(False)


@app.route("/check/project_titles", methods=["GET"])
def check_project_titles():
    Paccess = ProjectAccess()
    projects = Paccess.get_projects()

    given_letters = request.args.get('letters')

    possibilities = list()

    for proj in projects:
        if given_letters in proj.title:
            possibilities.append(proj.title)
            if len(possibilities) > 4:
                break

    return  jsonify(possibilities)


@app.route("/check/project_title_correct", methods=["GET"])
def check_project_title_correct():
    Paccess = ProjectAccess()
    projects = Paccess.get_projects()

    given_title = request.args.get('input')

    for proj in projects:
        if given_title == proj.title:
            return jsonify(True)

    return jsonify(False)


@login_manager.user_loader
def load_user(user_id):
    us = User(Session(user_id, 1, 0, 0))
    eAcces = EmployeeAccess()
    if user_id != 'None':
        us.roles = eAcces.get_employeeRoles(user_id)
    us.auth = True
    us.active = True
    return us


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('index'))


@app.route('/login/', methods=['POST'])
def login():
    us = User(Session(0, 1, 0, 0))
    username = request.form["username"]
    password = request.form["password"]
    try:
        if us.login(username, password):
            login_user(us)
            temp = current_user
            flash('Logged in successfully.')
            flash("you are now logged in")
            return "true"
        else:
            raise Exception('unable to log in, did you type your ussername or password correctly?')
    except:
        print("authentication error")
        return "false"


@app.route("/logout/", methods=['GET', 'POST'])
def logout():
    logout_user()
    next = request.args.get('logout')
    flash("you are now logged out")
    return redirect(next or url_for('index'))


if __name__ == "__main__":
    ip = config_data['ip']
    port = config_data['port']
    # temp=access.get_researchGroupOnID(1)
    # temp2=access.get_projectPromotors(1)
    # app.run(debug=True, host=ip, port=port, ssl_context=('../cert.pem', '../key.pem') )

    dbConnection.setConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                              dbhost=config_data['dbhost'])
    app.run(debug=True, host=ip, port=port)
