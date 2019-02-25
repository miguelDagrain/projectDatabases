# create table projectRegistration(
#   project int references project(projectID),
#   status registration,
#   student int references student(studentID),
#   PRIMARY KEY (project, status, student)
# );
from enum import Enum


class registration(Enum):
    Undefined = 0
    Bezig = 1
    Geslaagd = 2
    NietGeslaagd = 3


class dbProjectRegistration:
    def __init__(self, project, status, student):
        """
        a constructor for a dbProjectRegistration with all variables given
        :param project: an int representing a project id
        :param status: a registration Enum that represents the status of the registration
        :param student: an int that represent the studentId coupled to this registration
        :return:
        """
        self.m_project = project
        self.m_status = status
        self.m_student = student
