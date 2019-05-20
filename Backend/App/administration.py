from App.base import *
from App.utilities import login_required

from DataAccess.domainAccess import DomainAccess


@app.route("/administration/")
@login_required(role='admin')
def get_administration():
    """
    Creates an administration page. To view this page, the logged user needs the admin role.
    :return: Rendered template of administration.html
    """

    access = DomainAccess()
    disciplines = access.get_disciplines()
    types = access.get_projectType()
    return render_template("administration.html", page="administration", r_disciplines=disciplines, r_types=types)


@app.route("/administration/modify_disciplines", methods=["GET"])
@login_required(role='admin')
def form_modify_disciplines():
    """
    Function that returns a form to modify disciplines.
    The logged user needs the admin role.
    :return: Rendered template of the administration-modify-disciplines with disciplines
    """
    access = DomainAccess()
    disciplines = access.get_disciplines()

    return render_template("administration-modify-disciplines.html", r_disciplines=disciplines, send=False)


@app.route("/administration/modify_disciplines", methods=["POST"])
@login_required(role='admin')
def modify_disciplines():
    """
    Function that adds a discipline to the possible disciplines.
    :return: True if no exception is encountered, else false (both in string representation)
    """
    access = DomainAccess()
    disciplines = access.get_alldisciplines()
    actives = access.get_disciplines()

    value = request.form["discip"]
    try:
        if value:
            if value in disciplines and value not in actives:
                access.reactivate_discipline(value)
                return 'reactivated discipline'
            elif value not in disciplines:
                access.add_discipline(value)
                return 'true'
    except:
        return 'false'


@app.route("/administration/modify_disciplines", methods=["POST"])
@login_required(role='admin')
def remove_disciplines():
    """
    Function that removes a discipline to the possible disciplines
    :return: True if no exception is encountered, else false (both in string representation)
    """
    access = DomainAccess()
    disciplines = access.get_alldisciplines()

    value = request.form.get("Discipline")
    try:
        if value:
            discipline = disciplines[int(value)]
            access.remove_discipline(discipline)
        return 'true'
    except:
        return 'false'


@app.route("/administration/modify_types", methods=["POST"])
@login_required(role='admin')
def modify_types():
    """
    Function that modifies
    :return: True if no exception is encountered, else false (both in string representation)
    """
    access = DomainAccess()
    active = access.get_projectType()
    types = access.get_allprojectType()

    value = request.form["typ"]
    try:
        if value:
            if value in types and value not in active:
                access.reactivate_projectType(value)
                return 'reactivated type'

            elif value not in types:
                access.add_projectType(value)
                return 'true'
    except:
        return 'false'


@app.route("/administration/modify_types", methods=["POST"])
@login_required(role='admin')
def remove_types():
    """
    Function that removes a type
    :return: True if no exception is encountered, else false (both in string representation)
    """
    access = DomainAccess()
    types = access.get_allprojectType()

    try:
        value = request.form.get("Type")
        if value:
            type = types[int(value)]
            access.remove_type(type)
            return 'true'
    except:
        return 'false'