from App.base import *
from App.utilities import login_required

from DataAccess.projectAccess import ProjectAccess
from DataAccess.researchGroupAccess import ResearchGroupAccess
from DataAccess.domainAccess import DomainAccess
from DataAccess.employeeAccess import EmployeeAccess
from DataAccess.studentAccess import StudentAccess
from DataAccess.sessionAccess import SessionAccess
from MailService import MailService


@app.route("/projects/", methods=["GET"])
def show_projects():
    """
    Shows a list of all active projects on a HTML page
    :return: Rendered template of projects.html
    """
    pa=ProjectAccess()
    ra=ResearchGroupAccess()
    da=DomainAccess()

    projects = pa.get_project_filter_data(request.cookies.get("lang"))
    researchGroups = ra.get_researchGroups()

    if(current_user.is_authenticated):
        role = current_user.roles
        isAdmin= False
        for x in role:
            if x == "admin":
                isAdmin = True
        if isAdmin == True:
            disciplines = da.get_alldisciplines()
            types = da.get_allprojectType()
        else:
            disciplines = da.get_disciplines()
            types = da.get_projectType()
    else:
        disciplines = da.get_disciplines()
        types = da.get_projectType()

    projData = {}
    words = {}
    promoters = pa.get_promotors_and_associated_projects()
    supervisors = pa.get_supervisors_and_associated_projects()

    #print(supervisors, file=sys.stdout)

    rc = None
    su = current_user
    if su.is_authenticated:
        if su.session.EORS is EORS.STUDENT:
            rc = RelevanceCalculator(su.session.ID)
    for proj in projects:
        print( proj.researchGroup, file=sys.stdout)
        researchGroupNames = []
        for rg in proj.researchGroup:
            researchGroupNames.append(ra.get_researchGroupsOnIDs(rg)[0].name)


        typeNames = []
        for tp in proj.type:
            #print(tp, file=sys.stdout)
            typeNames.append(tp[0])

        print(proj.discipline, file=sys.stdout)
        disciplineNames = []
        for dc in proj.discipline:

            disciplineNames.append(dc)

        firstDescLines = "No description found."
        if request.cookies.get("lang") == "nl":
            firstDescLines = "Geen beschrijving gevonden."
        if len(proj.desc) > 0:
            firstDescLines = re.sub(r'<.+?>', '', proj.desc[0].text)
            tempDescLines = re.match(r'(?:[^.:;]+[.:;]){1}', firstDescLines)
            if (tempDescLines != None):
                firstDescLines = tempDescLines.group() + " ..."

        if rc is not None:
            pjson = {"ID": proj.ID, "title": proj.title, "status": proj.active, "type": typeNames, "tag": proj.tag,
                     "clickRelevance": rc.calculateProjectWeighting(proj.tag),
                     "disciplines": disciplineNames, "researchGroup": researchGroupNames,
                     "maxStudents": proj.maxStudents,
                     "registeredStudents": proj.registeredStudents, "description": firstDescLines}
        else:
            pjson = {"ID": proj.ID, "title": proj.title, "status": proj.active, "type": typeNames, "tag": proj.tag,
                     "clickRelevance": 1,
                     "disciplines": disciplineNames, "researchGroup": researchGroupNames,
                     "maxStudents": proj.maxStudents,
                     "registeredStudents": proj.registeredStudents, "description": firstDescLines}

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
                           words=json.dumps(words, default=lambda x: x.__dict__),
                           promoters=json.dumps(promoters, default=lambda x: x.__dict__),
                           supervisors=json.dumps(supervisors, default=lambda x: x.__dict__))


# Todo try catch and return result=false if exception encountered
@login_required(role="employee")
@app.route("/projects/", methods=["POST"])
def add_project():
    """
    Adds a project to the database. The project data is stored in a form in the request.
    :return: json formatted result (true or false)
    """

    # Get an access class
    da=DomainAccess()
    ea=EmployeeAccess()
    pa=ProjectAccess()

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
        if int(researchGroupNr) == 0:
            continue
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
    typeOptions = da.get_projectType()
    for typeNr in typeNrs:
        if int(typeNr) == 0:
            continue
        project.type.append(typeOptions[int(typeNr) - 1])

    # Append disciplines to the project
    disciplineOptions = da.get_disciplines()
    for disciplineNr in disciplineNrs:
        if int(disciplineNr) == 0:
            continue
        project.discipline.append(disciplineOptions[int(disciplineNr) - 1])

    # Fetch all employees from the database
    employeeOptions = ea.get_employees()

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
    relatedProjectOptions = pa.get_projects()
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
    pa.add_project(project)
    findTag(project)

    # Return result to javascript
    return jsonify(result=True)


@app.route("/projects/<int:id>", methods=['GET'])
def project_page(id):
    """
    Creates a project specific page for the project with ID = id.
    :param id: ID of the project
    :return: Rendered template of project.html
    """
    su = current_user
    if su.is_authenticated:
        if su.session.EORS is EORS.STUDENT:
            sa = SessionAccess()
            sa.add_sessionProjectClick(su.session.sessionID, id)
    Paccess = ProjectAccess()
    ea = EmployeeAccess()
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
        promotors.append(ea.get_employee(promotorID))

    staffIDs = Paccess.get_projectStaff(id)
    staff = list()
    for staffID in staffIDs:
        staff.append(ea.get_employee(staffID))

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


@login_required(role="employee")
@app.route('/projects/<int:id>/add_student', methods=['POST'])
def assign_student(id):
    """
    Assigns a student to a project
    :param id: Project to assign the student to
    :return: true or false (as string) false if encountered an exception, else true
    """
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


@app.route("/projects/<int:id>", methods=["POST"])
@login_required(role="employee")
def apply_remove_project(id):
    """
    Removes a project from the database
    :param id: ID of the project that needs to be removed
    :return:
    """
    Paccess = ProjectAccess()
    Paccess.remove_project(id)

    return redirect(url_for('show_projects'))


@app.route("/projects/search", methods=["GET"])
def apply_filter_projects():
    return redirect(url_for('show_projects'))


@app.route('/showInterest/', methods=['POST'])
def showInterest():
    # todo used?
    # message = request.form["Message"]
    message = "ik zijn eens geinteresseerd"
    sender = "miguel.dagraine@student.uantwerpen.be"  # todo: huidige persoon ingelogd moet nog opgehaald worden
    receiver = "thibautvangoethem2@gmail.com"  # todo: je moet nog kiezen welke promotor je de mail naar toestuurt verstuur het dan via ajax
    subject = "Expressing interest in " + "naam van project"  # todo: nog naam van project van project via ajax door sturen

    service = MailService()
    service.sendSingleMail(sender, receiver, subject, message)
    return True