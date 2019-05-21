from App.base import *
from App.utilities import login_required

from DataAccess.studentAccess import StudentAccess
from DataAccess.projectAccess import ProjectAccess


@login_required(role='student')
@app.route("/projects/add_bookmark/<int:id>/", methods=["GET"])
def add_bookmark(id):
    """
    Adds a bookmark for the currently logged user. (needs role student)
    :param id: ID of the project to create a bookmark for
    :return: redirect to project page
    """
    student = current_user.session.ID
    Access = StudentAccess()
    Access.add_bookmark(id, student)
    return redirect(url_for('project_page', id=id, added_bookmark=True))


@login_required(role='student')
@app.route("/bookmarks/", methods=['GET'])
def bookmark_page():
    """
    Creates a bookmark page based on the bookmarks of the student
    :return: Rendered template of bookmarks.html
    """
    student = current_user.session.ID

    sa = StudentAccess()
    pa = ProjectAccess()


    IDS = []
    bookmarks = sa.get_studentBookmarks(student)
    for bookmark in bookmarks:
        IDS.append(bookmark.project)

    projecten = []
    for project_id in IDS:
        project = pa.get_project(project_id)
        projecten.append(project)

    return render_template("bookmarks.html", b_projecten=projecten, page="bookmarks", empty=(len(projecten) == 0))


@app.route("/delete-bookmark/", methods=['POST'])
@login_required(role='student')
def remove_bookmark():
    """
    Removes a bookmark.
    :return: Redirection to bookmark page
    """
    project_id = request.form['project-id']
    student_id = current_user.session.ID
    pAccess = ProjectAccess()
    pAccess.remove_bookmark(project_id, student_id)
    return redirect(url_for('bookmark_page'))
