# create table session(
#   sessionID int unique not null,
#   startTime timestamp,
#   searchword varchar,
#   searchwordtime time,
#   clickedProject int references project(projectID),
#   clickedProjectTime time
# );

import time
class dbsession:
    m_sessionId=None
    m_starTime=None
    m_searchWordTime=None
    m_clickedProject=None
    m_clickedProjectTime=None

    def dbSession(self,sessionId,startTime,searchwordTime,clickedProject,clickedProjectTime):
        """
        a constructor for a dbSession with all variables given
        :param sessionId: an int representing the session
        :param startTime: a time object representing the time the session started
        :param searchwordTime: a time object representing when someone searched for a word
        :param clickedProject: an int referencing the projectID of the clicked project
        :param clickedProjectTime: a time object referencing the time the session clicked on a project
        :return: a new dbSession object
        """
        self.m_sessionId=sessionId
        self.m_starTime=startTime
        self.m_searchWordTime=searchwordTime
        self.m_clickedProject=clickedProject
        self.m_clickedProjectTime=clickedProjectTime
