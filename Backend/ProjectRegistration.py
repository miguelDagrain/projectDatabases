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

    def  __str__(self):
        return "project: "+self.project+", status: "+self.status+", student: "+str(self.student)