import json
import re
import sys
import datetime
import os
from functools import wraps
# from apscheduler.schedulers.background import BackgroundScheduler

from flask import *
from flask.templating import render_template
from flask_babel import *
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename

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

from helperFunc import *

app = Flask(__name__, template_folder="../html/templates/", static_folder="../html/static")
app_data = {'app_name': "newName"}
app.config['BABEL_TRANSLATION_DIRECTORIES'] = "../babel/translations/"
app.config['UPLOAD_FOLDER'] = "../attachments/"
app.config['HOME_PAGE_FOLDER'] = "../homepage/"
ALLOWED_EXTENSIONS = {'html', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
babel = Babel(app)
app.secret_key = b'&-s\xa6\xbe\x9b(g\x8a~\xcd9\x8c)\x01]\xf5\xb8F\x1d\xb2'
login_manager = LoginManager()
login_manager.init_app(app)


# uncomment this if you want to calculate tags
# findTags()


# overriding the login manager of flask login to support roles, inspired from 
# https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes 
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if (role not in current_user.roles) and (role != "ANY"):
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
    return redirect(url_for("home"))


@app.route("/home/")
def home():
    """
    Renders the index template
    :return: Rendered index template
    """

    this_dir = os.path.dirname(__file__)
    home_file = app.config['HOME_PAGE_FOLDER'] + 'homepage.html'
    try:
        homepage = open(os.path.join(this_dir, home_file), "r").read()
    # Store configuration file values
    except FileNotFoundError:
        homepage = ''
    # Keep preset values

    resp = make_response(render_template("home.html", page="index",
                                         homedoc=homepage, err=request.args.get('err', default=None)))
    if request.cookies.get('lang') is None:
        lang = get_locale()
        resp.set_cookie('lang', lang)
    return resp


@app.route("/home/", methods=["POST"])
def modify_homepage():
    """
    function to modify the home-page
    """

    if not os.path.isdir(app.config['HOME_PAGE_FOLDER']):
        os.mkdir(app.config['HOME_PAGE_FOLDER'])

    value = ""
    if request.form.get("newHome"):
        value = request.form.get("newHome")

    homeFile = open(app.config['HOME_PAGE_FOLDER'] + 'homepage.html', "w+")
    homeFile.write(value)
    homeFile.close()

    files = request.files.getlist("Attachments")

    print(files, file=sys.stdout)

    for file in files:
        print(file.filename, file=sys.stdout)
        nameFile = secure_filename(file.filename)
        file.save(os.path.join(app.config['HOME_PAGE_FOLDER'], nameFile))

    return jsonify(result=True)


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
    discipline = Daccess.get_disciplines()
    disciplines = []
    for row in discipline:
        if row[1] == 'true':
            disciplines.append(row[0])

    name = request.form.get("Name")
    abbrev = request.form.get("Abbreviation")
    disciplineNr = request.form.get("Discipline")
    discipline = disciplines[int(disciplineNr)]
    active = True  # active wordt gebruikt voor leesbaarheid
    address = request.form.get("Address")
    telephone = request.form.get("Telephone")
    # desc = request.form.get("Description")
    desc = list()  # TODO : dit aanpassen zodat het nieuwe descripties kan aanemen (nu ga ik het gewoon document 1 eraan kopellen)

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
    researchGroup = Racces.get_singleResearchGroupOnID(id)

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
        toadd = False
        for rgroup in project.researchGroup:
            if rgroup == researchGroup.ID:
                toadd = True
        if (toadd):
            projects.append(project)

    language = request.cookies.get('lang')
    description = None
    for doc in researchGroup.desc:
        if doc.language == language:
            description = doc.text

    return render_template("researchgroup.html", r_groupName=researchGroup.name, r_groupID=researchGroup.ID,
                           r_description=description, r_researchers=researchers, r_contactPersons=contactPersons,
                           r_projects=projects, page='rgroups')


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
        Eaccess = EmployeeAccess()
        people = Eaccess.get_employees()
        # researchGroupOptions = [""]
        #
        # for iter in researchGroups:
        #     researchGroupOptions.append(iter.name)
        #
        # name = request.args.get("Name")
        # groupNr = int(request.args.get("Research_group"))
        # group = researchGroupOptions[groupNr]
        # promotor = int(request.args.get("Promotor"))
        #
        # people = Raccess.filter_employees(name, group, promotor)

    neededValuesPeoplePage = {}
    for person in people:
        for group in researchGroups:
            if group.ID == person.research_group:
                neededValuesPeoplePage[person.id] = {"name": person.name, "group": group.name,
                                                     "promotor": person.promotor, "ID": person.id}
                # neededValuesPeoplePage.append([person.name, group.name, person.promotor, person.id])

    return render_template("people.html", r_values=json.dumps(neededValuesPeoplePage, default=lambda x: x.__dict__),
                           r_researchGroups=researchGroups,
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
    active = True  # active wordt gebruikt voor leesbaarheid
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
    group = Raccess.get_singleResearchGroupOnID(person.research_group)

    projects = person.getProjects()

    yearAndProject = dict()

    for project in projects:
        for year in project.activeYear:
            if (year in yearAndProject):
                yearAndProject[year].append(project)
            else:
                yearAndProject[year] = list()
                yearAndProject[year].append(project)

    orderedYearAndProject = sorted(yearAndProject.items(), key=lambda k: k[0], reverse=True)

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

        firstDescLines = "No description found."
        if len(proj.desc) > 0:
            firstDescLines = re.sub(r'<.+?>', '', proj.desc[0].text)
            tempDescLines = re.match(r'(?:[^.:;]+[.:;]){1}', firstDescLines)
            if (tempDescLines != None):
                firstDescLines = tempDescLines.group() + " ..."

        pjson = {"ID": proj.ID, "title": proj.title, "status": proj.active, "type": typeNames, "tag": proj.tag,
                 "disciplines": disciplineNames, "researchGroup": researchGroupNames, "maxStudents": proj.maxStudents,
                 "registeredStudents": proj.registeredStudents, "description": firstDescLines}

        # print(proj.tag[0], file=sys.stdout)

        for d in proj.desc:
            textstr = d.text
            rgx = re.compile("(\w[\w']*\w|\w)")
            list = rgx.findall(textstr)
            for w in list:
                if not w in words:
                    words[w] = {}
                    words[w]["total"] = 0

                if str(proj.ID) in words[w]:
                    words[w][str(proj.ID)] += 1
                    words[w]["total"] += 1
                else:
                    words[w][str(proj.ID)] = 1
                    words[w]["total"] += 1

        projData[proj.ID] = pjson

    return render_template("projects.html", r_researchGroups=researchGroups,
                           r_disciplines=disciplines, r_types=types, page="projects",
                           alt=json.dumps(projData, default=lambda x: x.__dict__),
                           words=json.dumps(words, default=lambda x: x.__dict__))


@app.route("/projects/", methods=["POST"])
def add_project():
    # Get an access class
    access = FullDataAccess()

    # Acquire form data
    title = request.form["Title"]
    maxStudents = request.form["Maxstudents"]
    descriptionTextNl = request.form["nlDescription"]
    descriptionTextEng = request.form["engDescription"]

    researchGroupNrs = request.form.getlist("Researchgroup")
    typeNrs = request.form.getlist("Type")
    disciplineNrs = request.form.getlist("Discipline")
    tags = request.form.getlist("Tags")
    related = request.form.getlist("Related")
    promotorNames = request.form.getlist("Promotors")
    supervisorNames = request.form.getlist("Supervisors")
    externNames = request.form.getlist("Extern")

    # Acquire request files
    files_nl = request.files.getlist("nlUploads")
    files_en = request.files.getlist("engUploads")

    # Create basic project
    project = Project(None, title, maxStudents, True)

    # Assign research group ID's
    for researchGroupNr in researchGroupNrs:
        project.researchGroup.append(int(researchGroupNr))

    # Create dutch document
    docNL = Document(None, "dutch", descriptionTextNl)
    # Link attachments to document
    for file in files_nl:
        nameFile = secure_filename(title + '_' + file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nameFile))
        docNL.attachment.append(nameFile)
    # Assign document as description
    project.desc.append(docNL)

    # Create english document
    docEn = Document(None, "english", descriptionTextEng)
    # Link attachments to document
    for file in files_en:
        nameFile = secure_filename(title + '_' + file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nameFile))
        docEn.attachment.append(nameFile)
    # Assign document as description
    project.desc.append(docEn)

    # Append types to the project
    typeOptions = access.get_projectType()
    for typeNr in typeNrs:
        project.type.append(typeOptions[int(typeNr) - 1])

    # Append disciplines to the project
    for disciplineNr in disciplineNrs:
        project.discipline.append(int(disciplineNr))

    # Fetch all employees from the database
    employeeOptions = access.get_employees()

    # Add promotors to the project
    # Create dictionary of promotor name and his id, used to easily append ID to the project
    promotor_id_dict = {promotorOption.name: promotorOption.id for promotorOption in employeeOptions}
    # Loop over names and connect the associated ID's to the project
    for promotorName in promotorNames:
        if promotorName in promotor_id_dict:
            project.promotors.append(promotor_id_dict[promotorName])

    # Add supervisors to the project
    # Create dictionary of supervisor name and his id, used to easily append ID to the project
    supervisor_id_dict = {staffOption.name: staffOption.id for staffOption in
                          employeeOptions}
    # Loop over names and connect the associated ID's to the project
    for staffName in supervisorNames:
        if staffName in supervisor_id_dict:
            project.supervisors.append(supervisor_id_dict[staffName])

    # Add extern employees to the project
    for name in externNames:
        project.extern_employees.append(name)

    # Add tags to the project
    project.tag = list(tags)

    # Add related projects to the project
    # Fetch all projects from the database
    relatedProjectOptions = access.get_projects()
    # Create dictionary of project title and its id, used to easily find the required ID
    related_project_id_dict = {relatedProjectOption.title: relatedProjectOption.ID for relatedProjectOption in
                               relatedProjectOptions}
    # Loop over related projects and append the associated ID to the project relations
    for relatedProjectTitle in related:
        if relatedProjectTitle in related_project_id_dict:
            project.relatedProject.append(related_project_id_dict[relatedProjectTitle])

    # Assign active year
    now = datetime.now()
    project.activeYear.append(now.year)

    # Finalize project and add it to the database
    access.add_project(project)

    # Return result to javascript
    return jsonify(result=True)


# TODO meerdere promotors kunnen in 1 project, geeft nu enkel 1 weer
@app.route("/projects/<int:id>", methods=['GET'])
def project_page(id):
    su = current_user
    if su.is_authenticated:
        if su.session.EORS is EORS.STUDENT:
            sa = SessionAccess()
            sa.add_sessionProjectClick(su.session.sessionID, id)
    Paccess = ProjectAccess()
    Eaccess = EmployeeAccess()
    Raccess = ResearchGroupAccess()
    project = Paccess.get_project(id)
    promotorsIDs = Paccess.get_projectPromotors(id)
    documents = Paccess.get_projectDocuments(id)
    document = Document(None, None, None)
    if request.cookies.get("lang") == 'nl':
        for d in documents:
            if d.language == 'dutch':
                document = d
    else:
        for d in documents:
            if d.language == 'english':
                document = d

    # If for some reason there is no text, select a document with text
    if document.text is None or document.text == "":
        for d in documents:
            if d.text is not None and d.text != "":
                document = d
                break

    promotors = list()
    for promotorID in promotorsIDs:
        promotors.append(Eaccess.get_employee(promotorID))

    staffIDs = Paccess.get_projectStaff(id)
    staff = list()
    for staffID in staffIDs:
        staff.append(Eaccess.get_employee(staffID))

    extern = project.extern_employees

    researchGroups = Raccess.get_researchGroupsOnIDs(project.researchGroup)
    docattachments = document.attachment

    if len(staff) == 0:
        staff = None
    if len(promotors) == 0:
        promotors = None
    if len(docattachments) == 0:
        docattachments = None
    if len(extern) == 0:
        extern = None

    return render_template("project.html", r_project=project, r_promotors=promotors, supervisors=staff, desc=document,
                           r_researchGroups=researchGroups, page="projects", r_attachments=docattachments,
                           extern=extern, added_bookmark=request.args.get('added_bookmark', default=False))


@app.route('/projects/<int:id>/add_student', methods=['POST'])
def add_student(id):
    sid = request.form["sid"]
    try:
        if len(sid) != 8:
            raise Exception('student id not the right size')
        if sid[0] == 's' or sid[0] == 'S':
            sid = sid[1:]
            sid = '2' + sid

        sa = StudentAccess()
        stu = sa.get_studentOnStudentNumber(sid)
        if stu is None:
            raise Exception('student doesnt exist')
        pa = ProjectAccess()
        proj = pa.get_project(id)
        if proj is None:
            raise Exception('project doesnt exist')
        registrations = sa.get_projectRegistrationsOnProject(id)
        if len(registrations) >= proj.maxStudents:
            raise Exception('project already has maximum amount of students')
        for i in registrations:
            if i.student == sid:
                raise Exception('student already registered for this project')
        sa.add_projectRegistration(id, stu.studentID)
        return 'true'
    except:
        return 'false'


@app.route('/download/<string:name>', methods=['GET'])
def download(name):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=name, as_attachment=True)


@app.route('/download_homepage/<string:name>', methods=['GET'])
def download_homepage(name):
    return send_from_directory(directory=app.config['HOME_PAGE_FOLDER'], filename=name, as_attachment=True)


@app.route("/projects/<int:id>", methods=["POST"])
def apply_remove_project(id):
    Paccess = ProjectAccess()
    Paccess.remove_project(id)

    return redirect(url_for('show_projects'))


@login_required(role='student')
@app.route("/projects/<int:id>/<int:empty>", methods=["GET"])
def add_bookmark(id, empty):
    student = current_user.session.ID
    Access = StudentAccess()
    Access.add_bookmark(id, student)
    return redirect(url_for('project_page', id=id, added_bookmark=True))


@login_required(role='student')
@app.route("/bookmarks/", methods=['GET'])
def bookmark_page():
    student = current_user.session.ID

    Access = StudentAccess()
    fullAccess = FullDataAccess()

    IDS = []
    bookmarks = Access.get_studentBookmarks(student)
    for bookmark in bookmarks:
        IDS.append(bookmark.project)

    projecten = []
    for project_id in IDS:
        project = fullAccess.get_project(project_id)
        projecten.append(project)

    return render_template("bookmarks.html", b_projecten=projecten, page="bookmarks", empty=(len(projecten) == 0))


@app.route("/delete-bookmark/", methods=['POST'])
@login_required(role='student')
def remove_bookmark():
    project_id = request.form['project-id']
    student_id = current_user.session.ID
    pAccess = ProjectAccess()
    pAccess.remove_bookmark(project_id, student_id)
    return redirect(url_for('bookmark_page'))


@app.route("/projects/search", methods=["GET"])
def apply_filter_projects():
    # if request.args.get("Search_query") is None:
    #     return show_projects()
    # else:
    #     Raccess = ResearchGroupAccess()
    #     researchGroups = Raccess.get_researchGroups()
    #     typeOptions = ["", "Bachelor dissertation", "Master thesis", "Research internship 1", "Research internship 2"]
    #     Daccess = DomainAccess()
    #     disciplineOptions = Daccess.get_disciplines()
    #     researchGroupOptions = [""]
    #
    #     for iter in researchGroups:
    #         researchGroupOptions.append(iter.name)
    #
    #     query = request.args.get("Search_query")
    #     print(query, file=sys.stderr)
    #     typeNr = int(request.args.get("Type"))
    #     type = typeOptions[typeNr]
    #
    #     disciplineNrs = request.args.getlist("Disciplines")
    #     discipline = helper_get_selected_multi_choice(disciplineNrs, disciplineOptions)
    #
    #     groupNr = int(request.args.get("Research_group"))
    #     group = researchGroupOptions[groupNr]
    #     status = int(request.args.get("Status"))
    #
    #     Paccess = ProjectAccess()
    #     projects = Paccess.filter_projects(query, type, discipline, group, status)
    #
    # return render_template("projects.html", r_projects=projects, r_researchGroups=researchGroups,
    #                        r_disciplines=disciplineOptions, r_types=typeOptions, page="projects",
    #                        alt=json.dumps(projects, default=lambda x: x.__dict__))
    return redirect(url_for('show_projects'))


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
    disciplines = access.get_alldisciplines()
    actives = access.get_disciplines()

    value = request.form.get("Name")
    if value:
        if value in disciplines and value not in actives:
            access.reactivate_discipline(value)
        elif value not in disciplines:
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
    access = DomainAccess()
    types = access.get_projectType()

    return render_template("administration-modify-types.html", r_types=types, send=False)
    # access = DomainAccess
    # types = access.get_projectType()


@app.route("/administration/modify_types", methods=["POST"])
def modify_types():
    """
    function that modifies
    :return:
    """
    access = DomainAccess()
    active = access.get_projectType()
    types = access.get_allprojectType()

    value = request.form.get("Name")
    if value:
        if value in types and value not in active:
            access.reactivate_projectType(value)

        elif value not in types:
            access.add_projectType(value)
    else:
        value = request.form.get("Type")
        if value:
            type = types[int(value)]
            access.remove_type(type)

    # disciplines = access.get_disciplines()
    return render_template("administration-modify-types.html", send=True)


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

    return jsonify(possibilities)


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
    eors = EORS.UNKNOWN
    if (user_id[0] == "S"):
        sa = SessionAccess()
        se = sa.get_SessionOnId(user_id[1:])
        us = User(se)

        # eors = EORS.STUDENT
        # us = User(Session(0, user_id[1:], 0, eors))
    elif (user_id[0] == "E"):
        eors = EORS.EMPLOYEE
        us = User(Session(0, user_id[1:], 0, eors))

    eAcces = EmployeeAccess()
    us.roles = list()
    if user_id != 'None' and us.session.EORS == EORS.EMPLOYEE:
        us.roles = eAcces.get_employeeRoles(user_id[1:])
        us.roles.append("employee")
    elif user_id != 'None' and us.session.EORS == EORS.STUDENT:
        us.roles.append('student')
    us.auth = True
    us.active = True
    return us


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('home', err="login_required"))


@app.route('/login/', methods=['POST'])
def login():
    sa = SessionAccess()
    us = User(Session(None, 1, sa.get_CurentSQLTime(), EORS.UNKNOWN))
    username = request.form["username"]
    password = request.form["password"]
    try:
        if us.login(username, password):
            if (us.session.EORS == EORS.STUDENT):
                sa.add_Session(us.session)
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
    if (current_user.session.EORS == EORS.STUDENT):
        us = current_user
        sa = SessionAccess()
        sa.add_Session(us.session)
    logout_user()
    next = request.args.get('logout')
    flash("you are now logged out")
    return redirect(next or url_for('index'))


@app.route('/upload/')
def upload():
    return render_template('uploader.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + "test/"):
                os.mkdir(app.config['UPLOAD_FOLDER'] + "test/")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "test/" + filename))

            # return redirect(url_for('uploaded_file',filename=filename))
    return 'file uploaded successfully'


@app.route('/showInterest/', methods=['POST'])
def showInterest():
    # message = request.form["Message"]
    message = "ik zijn eens geinteresseerd"
    sender = "miguel.dagraine@student.uantwerpen.be"  # todo: huidige persoon ingelogd moet nog opgehaald worden
    receiver = "thibautvangoethem2@gmail.com"  # todo: je moet nog kiezen welke promotor je de mail naar toestuurt verstuur het dan via ajax
    subject = "Expressing interest in " + "naam van project"  # todo: nog naam van project van project via ajax door sturen

    service = MailService()
    service.sendSingleMail(sender, receiver, subject, message)
    return True


@app.route('/profile/')
@login_required(role='employee')
def emp_profile():
    access = ProjectAccess()
    if current_user.session.EORS != EORS.EMPLOYEE:
        return redirect(url_for("index"))
    id = current_user.session.ID
    projects = access.get_projects_of_employee(id)
    inactive_count = access.get_number_of_inactive_by_employee(id)
    return render_template("emp_profile.html",
                           projects=projects,
                           inactive=inactive_count,
                           page='profile',
                           err=request.args.get('err', default=False, type=bool),
                           update=request.args.get('update', default=False, type=bool),
                           removed=request.args.get('removed', default=False, type=bool)
                           )


@app.route('/profile/', methods=['POST'])
@login_required(role='employee')
def change_project():
    # Fetch data from HTML
    project_id = request.form['project-id']
    new_title = request.form['project-title']
    desc_nl_id = request.form['desc-nl-id']
    desc_en_id = request.form['desc-en-id']
    new_desc_nl = request.form['desc-nl']
    new_desc_en = request.form['desc-en']

    # Database Access instances
    pAccess = ProjectAccess()
    dAccess = DocumentAccess()

    # Create new document if necessary
    # Dutch document:
    if desc_nl_id == '' and new_desc_nl is not None:
        new_doc = Document(-1, 'dutch', new_desc_nl)
        new_doc = pAccess.add_projectDocument(project_id, new_doc)
        desc_nl_id = str(new_doc.ID)
    # English document:
    if desc_en_id == '' and new_desc_en is not None:
        new_doc = Document(-1, 'english', new_desc_en)
        new_doc = pAccess.add_projectDocument(project_id, new_doc)
        desc_en_id = str(new_doc.ID)

    # Apply changes
    if pAccess.change_title(project_id, new_title) and \
            dAccess.update_document_text(desc_en_id, new_desc_en) and \
            dAccess.update_document_text(desc_nl_id, new_desc_nl):
        return redirect(url_for('emp_profile', update=True))
    else:
        return redirect(url_for('emp_profile', err=True))


@app.route('/profile/remove', methods=['POST'])
@login_required(role='employee')
def remove_project():
    id = request.form['project-id']
    apply_remove_project(id)
    return redirect(url_for('emp_profile', removed=True))


if __name__ == "__main__":
    ip = config_data['ip']
    port = config_data['port']
    # temp=access.get_researchGroupOnID(1)
    # temp2=access.get_projectPromotors(1)
    # app.run(debug=True, host=ip, port=port, ssl_context=('../cert.pem', '../key.pem') )
    dbConnection.setConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'], dbpass=config_data['dbpass'],
                               dbhost=config_data['dbhost'])

    # mailer = MailService()
    #
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(mailer.sendMailExtendingFirst(),trigger='cron', minute='0', hour='0', day='10', month='9', year='*')
    # scheduler.add_job(mailer.sendMailExtendingSecond(), trigger='cron', minute='0', hour='0', day='20', month='9',year='*')
    # scheduler.add_job(deactivate_projects(), trigger='cron', minute='0', hour='0', day='25', month='9',year='*')
    app.run(debug=True, host=ip, port=port)

