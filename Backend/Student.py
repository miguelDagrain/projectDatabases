class Student:
    def __init__(self, student_id, name):
        """
        a constructor for a dbStudent with all variables given
        :param name: a string representing the name of the student
        :param student_id: an int that is the id for the student
        :param liked_project: an int referencing the projectId of all the projects the student liked(bookmarked)
        :param session: an int referencing the sessionId of an open session that the student is using
        :return: a new dbStudent object
        """
        self.name = name
        self.studentID = student_id
        self.likedProject = list()

    def get_likedProjects(self, dbconnect):
        access = __import__('DataAccess', fromlist=['ProjectAccess'])
        pro = access.ProjectAccess(dbconnect)
        projects = list()
        for i in self.likedProject:
            projects.append(pro.get_project(i))
        return projects
