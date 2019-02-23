# create table student(
#   name varchar(70) NOT NULL ,
#   studentID int not null unique primary key,
#   likedProject int references project(projectID),
#   session int references session(sessionID)
# );

class dbStudent:
    m_name=None
    m_studentID=None
    m_likedProject=None
    m_session=None
    def dbStudent(self,name,studentID,likedProject,session):
        """
        a constructor for a dbStudent with all variables given
        :param name: a string representing the name of the studen
        :param studentID: an int that is the id for the student
        :param likedProject: an int referencing the projectId of a project the student liked
        :param session: an int referncing the sessionId of an open session that the studen is using
        :return: a new dbStudent object
        """
        self.m_name=name
        self.m_studentID=studentID
        self.m_likedProject=likedProject
        self.m_session=session
