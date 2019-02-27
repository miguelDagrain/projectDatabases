# create table student(
#   name varchar(70) NOT NULL ,
#   studentID int not null unique primary key,
#   likedProject int references project(projectID),
#   session int references session(sessionID)
# );

class Student:
    def __init__(self, name, student_id, liked_project, session):
        """
        a constructor for a dbStudent with all variables given
        :param name: a string representing the name of the student
        :param student_id: an int that is the id for the student
        :param liked_project: an int referencing the projectId of a project the student liked
        :param session: an int referencing the sessionId of an open session that the student is using
        :return: a new dbStudent object
        """
        self.name = name
        self.studentID = student_id
        self.likedProject = liked_project
        self.session = session
