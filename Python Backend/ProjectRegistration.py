# create table projectRegistration(
#   project int references project(projectID),
#   status registration,
#   student int references student(studentID),
#   PRIMARY KEY (project, status, student)
# );
from enum import Enum


class Registration(Enum):
    UNDEFINED = 0
    BUSY = 1
    FINISHED = 2
    NOT_FINISHED = 3


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
