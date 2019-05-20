from App.base import *
from App.utilities import login_required

from DataAccess.researchGroupAccess import ResearchGroupAccess
from DataAccess.domainAccess import DomainAccess
from DataAccess.employeeAccess import EmployeeAccess
from DataAccess.projectAccess import ProjectAccess


@login_required(role='admin')
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
    return render_template("researchgroups.html", r_groups=groups, r_disciplines=disciplines, page="administration")


@app.route("/researchgroups/", methods=["POST"])
def add_research_group():
    """
    Adds a research group to the database
    This function is called whenever the user uses the POST method on the research group page
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
    active = True  # active is used for readability
    address = request.form.get("Address")
    telephone = request.form.get("Telephone")
    # desc = request.form.get("Description")
    desc = list()

    r = ResearchGroup(None, name, abbrev, discipline, active, address, telephone, desc)
    Raccess = ResearchGroupAccess()
    Raccess.add_researchGroup(r)
    researchGroups = Raccess.get_researchGroups()
    return render_template("researchgroups.html", r_groups=researchGroups, r_disciplines=disciplines,
                           page="administration")


@app.route("/researchgroups/<int:id>", methods=["GET"])
def group_page(id):
    """
    Renders a template with the research group specific information.
    This page shows the projects connected to the research group and its members
    :param id: the id of the researchgroup
    :return: rendered template of the groups page
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
                           r_projects=projects, page='administration')


@app.route("/researchgroups/<int:id>", methods=["POST"])
def apply_remove_group(id):
    """
    Function that removes a research group and redirects to the research groups page
    :param id: id of the group to be removed
    :return: redirection to research groups page
    """

    Racces = ResearchGroupAccess()
    Racces.remove_researchGroup(id)

    return redirect(url_for('show_research_groups'))
