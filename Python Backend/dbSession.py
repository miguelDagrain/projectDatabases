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
    def __init__(self, sessionId, startTime, searchWordTime, clickedProject, clickedProjectTime):
        """
        a constructor for a dbSession with all variables given
        :param sessionId: an int representing the session
        :param startTime: a time object representing the time the session started
        :param searchWordTime: a time object representing when someone searched for a word
        :param clickedProject: an int referencing the projectID of the clicked project
        :param clickedProjectTime: a time object referencing the time the session clicked on a project
        :return: a new dbSession object
        """
        self.sessionId = sessionId
        self.startTime = startTime
        self.searchWordTime = searchWordTime
        self.clickedProject = clickedProject
        self.clickedProjectTime = clickedProjectTime
