from App.base import *
from App.utilities import login_required

from DataAccess.employeeAccess import EmployeeAccess
from DataAccess.researchGroupAccess import ResearchGroupAccess
from DataAccess.domainAccess import DomainAccess


@app.route("/people/", methods=["GET"])
@login_required(role='admin')
def show_people():
    """
    Shows a table of people on a html page
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

    neededValuesPeoplePage = {}
    for person in people:
        for group in researchGroups:
            if group.ID == person.research_group:
                neededValuesPeoplePage[person.id] = {"name": person.name, "group": group.name,
                                                     "promotor": person.promotor, "ID": person.id}

    return render_template("people.html", r_values=json.dumps(neededValuesPeoplePage, default=lambda x: x.__dict__),
                           r_researchGroups=researchGroups,
                           page="administration")


@app.route("/people/", methods=["POST"])
def add_staff():
    """
    Function that adds a staff member to the database, is called every time the user uses the POST method on the
    add staff form of the people page
    :return: redirection to show people page
    """

    Daccess = DomainAccess()
    name = request.form.get("Name")
    email = request.form.get("Email")
    office = request.form.get("Office")
    researchgroupNr = request.form.get("Researchgroup")
    research_group = int(researchgroupNr)+1
    titleOptions = Daccess.get_titles()
    titleNr = request.form.get("Title")
    title = titleOptions[int(titleNr)]
    roleOptions = Daccess.get_intextOrigin()
    roleNr = request.form.get("Role")
    role = roleOptions[int(roleNr)]
    active = True  # active is used for readability
    promotor = True if request.form.get("Promotor") == 'on' else False

    emp = Employee(None, name, email, office, research_group, title, role, active, promotor)
    Eaccess = EmployeeAccess()
    Eaccess.add_employee(emp)
    return redirect(url_for('show_people'))


@app.route("/people/<int:id>", methods=["GET"])
def get_person(id):
    """
    Function that return a tab of the person whose id equals the parameter id
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
    unknownlist=list()
    for project in projects:
        if(len(project.activeYear) is 0):
            unknownlist.append(project)
    orderedYearAndProject.append(("unknown year",unknownlist))
    return render_template("person.html", r_person=person, r_groupName=group.name,
                           r_projectAndYear=orderedYearAndProject, page="administration")


@app.route("/people/<int:id>", methods=["POST"])
def apply_remove_person(id):
    """
    function that removes the person on whose id equals the parameter id
    :param id: id of the person to be removed
    :return: redirection to show_people
    """
    Eaccess = EmployeeAccess()
    Eaccess.remove_employee(id)

    return redirect(url_for('show_people'))
