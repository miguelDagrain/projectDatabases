class ProjectRegistration:
    def __init__(self, project, status, student):
        """
        a constructor for a dbProjectRegistration with all variables given
        :param project: an int representing a project id
        :param status: a registration Enum that represents the status of the registration
        :param student: an int that represent the studentId coupled to this registration
        :return:
        """
        self.project = project
        self.status = status
        self.student = student

    def get_student(self, connect):
        from DataAccess.studentAccess import StudentAccess
        sa = StudentAccess()
        return sa.get_student(self.student)

    def getProject(self, dbconnect):
        access = __import__('DataAccess', fromlist=['ProjectAccess'])
        from DataAccess.projectAccess import ProjectAccess
        pro = ProjectAccess()
        return pro.get_project(self.project)
