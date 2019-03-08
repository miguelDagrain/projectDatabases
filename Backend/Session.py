# create table session(
#   sessionID int unique not null,
#   startTime timestamp,
#   searchword varchar,
#   searchwordtime time,
#   clickedProject int references project(projectID),
#   clickedProjectTime time
# );


class Session:
    def __init__(self, session_id, student_id,start_time,start_date):
        """
        a constructor for a dbSession with all variables given
        :param session_id: an int representing the session
        :param start_time: a time object representing the time the session started
        :param search_word_time: a time object representing when someone searched for a word
        :param clicked_project: an int referencing the projectID of the clicked project
        :param clicked_project_time: a time object referencing the time the session clicked on a project
        :return: a new dbSession object
        """
        self.studentId=student_id
        self.sessionId = session_id
        self.startTime = start_time
        self.startDate = start_date
        #both list of tuples
        self.searchWords=list()
        self.clickedProjects = list()

    def __str__(self):
        return "id: "+str(self.sessionId)+", startTime: "+self.startTime+", searchWordTime: "+self.searchWordTime+", clickedProject: "+self.clickedProject+", clickedProjectTime: "+self.clickedProjectTime