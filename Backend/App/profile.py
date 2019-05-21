from App.base import *
from App.utilities import login_required

from DataAccess.projectAccess import ProjectAccess
from DataAccess.documentAccess import DocumentAccess


@app.route('/profile/')
@login_required(role='employee')
def emp_profile():
    """
    Creates a profile page for an employee.
    :return: Rendered template of profile.html
    """
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
                           deactivate=request.args.get('deactivate', default=False, type=bool),
                           activate=request.args.get('activate', default=False, type=bool)
                           )


@app.route('/profile/', methods=['POST'])
@login_required(role='employee')
def change_project():
    """
    Changes a project
    :return: redirect to employee profile
    """
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


@app.route('/profile/state', methods=['POST'])
@login_required(role='employee')
def change_project_status():
    """
    Removes a project from the database
    :return: redirection to employee profile
    """
    id = request.form['project-id']
    pAccess = ProjectAccess()
    p = pAccess.get_project(id)

    pAccess.change_project_active(id, p.active)

    if p.active:
        return redirect(url_for('emp_profile', deactivate=True))
    elif p.active is False:
        return redirect(url_for('emp_profile', activate=True))
    else:
        return redirect(url_for('emp_profile', err=True))
