from enum import Enum
#enum to denote employee or student
class EORS(Enum):
    UNKNOWN=0
    STUDENT=1
    EMPLOYEE=2

class Session:
    def __init__(self, session_id, id, start_time, start_date, EORS):
        """
        a constructor for a dbSession with all variables given
        :param session_id: an int representing the session
        :param start_time: a time object representing the time the session started
        :param search_word_time: a time object representing when someone searched for a word
        :param clicked_project: an int referencing the projectID of the clicked project
        :param clicked_project_time: a time object referencing the time the session clicked on a project
        :return: a new dbSession object
        """
        self.studentId = id
        self.sessionId = session_id
        self.startTime = start_time
        self.startDate = start_date
        # both list of tuples
        self.searchWords = list()
        self.clickedProjects = list()
        self.EORS=EORS

    def get_clickedProjects(self, dbconnect):
        access = __import__('DataAccess', fromlist=['ProjectAccess'])
        pro = access.ProjectAccess(dbconnect)
        projects = list()
        for i in self.clickedProjects:
            projects.append(pro.get_project(i))
        return projects

    def get_student(self, dbconnect):
        access = __import__('DataAccess', fromlist=['StudentAccess'])
        sa = access.StudentAccess(dbconnect)
        return sa.get_student(self.studentId)
