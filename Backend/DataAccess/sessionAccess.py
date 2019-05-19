import dbConnection

class SessionAccess:
    def __init__(self):
        """
        constructor for a SessionAccess object
        """
        self.dbconnect = dbConnection.connection

    def get_SessionOnId(self,id):
        """
        getter for a single session based on the session id
        :param id: the sessionid
        :return: a session object
        """
        from Session import Session
        from Session import EORS
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('select * from Session where sessionID=%s' ,(str(id),))
            row=cursor.fetchone()
            session = Session(row[0],row[1],row[2],EORS.STUDENT)
            cursor.execute('select * from sessionProjectClick where sessionID=%s',(str(id),))
            for i in cursor:
                session.clickedProjects.append(i[1])

            return session
        except Exception as e:
            print('error while getting session on id '+str(e))
            return None

    def get_SessionOnSID(self,studentID):
        """
        gets all the session that belong to a certain studentid
        :param studentID: the studentID
        :return:a list of sessions
        """
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('select * from Session where studentID=%s', (str(studentID),))
            sessions=list()
            for row in cursor:
                sessions.append(self.getSessionOnId(row[0]))
            return sessions
        except Exception as e:
            print('error while getting session on id ' + str(e))
        return None

    def add_Session(self, session):
        """
        adds a session to the database
        :param session: the new session
        """
        from Session import EORS
        if(session.EORS!=EORS.STUDENT):
            return
        try:
            cursor = self.dbconnect.get_cursor()
            if(session.sessionID is not None):
                cursor.execute('select * from  Session where sessionID=%s',(str(session.sessionID),) )
                if(cursor.rowcount!=0):
                    self.change_Session(session)
                    return
                cursor.execute('insert into Session values(%s,%s,%s)',(str(session.sessionID),str(session.ID),str(session.startTime)))
            else:
                cursor.execute('insert into Session values(DEFAULT,%s,%s) returning sessionID',
                               ( str(session.ID), str(session.startTime)))

                session.sessionID=cursor.fetchone()[0]
            self.dbconnect.commit()
            for i in session.clickedProjects:
                cursor.execute('execute insertClick(%s,%s)',(str(session.sessionID),str(i)))
            self.dbconnect.commit()
        except Exception as e:
            print('error while adding session ' + str(e))
            self.dbconnect.rollback()

    def change_Session(self,session):
        """
        changes the values of a session that already is in the database
        :param session: the session you are cahnging
        """
        from Session import EORS
        if (session.EORS != EORS.STUDENT):
            return
        try:
            cursor=self.dbconnect.get_cursor()
            if (session.sessionID is not None):
                cursor.execute('update session set studentID=%s, startTime=%s where sessionID=%s',
                               (str(session.ID),str(session.startTime),str(session.sessionID)))
                cursor.execute('delete from sessionProjectClick where sessionID=%s',(str(session.sessionID),))
                self.dbconnect.commit()
                for i in session.clickedProjects:
                    cursor.execute('execute insertClick(%s,%s)', (str(session.sessionID), str(i)))
            self.dbconnect.commit()
        except Exception as e:
            print('error while changing session ' + str(e))
            self.dbconnect.rollback()

    def add_sessionProjectClick(self,sessionID,projectID):
        """
        adds a session project click that binds a sessionid and a projectid
        :param sessionID:
        :param projectID:
        """
        try:
            cursor=self.dbconnect.get_cursor()
            cursor.execute('execute insertSessionProjectClick(%s,%s)',(str(sessionID),str(projectID),))
            self.dbconnect.commit()
        except Exception as e:
            print('unable to add sessionProjectClick'+str(e))
            self.dbconnect.rollback()

    def get_CurentSQLTime(self):
        """
        a quick function that returns the NOW() time of sql, this time should be used in the session classes
        :return: a string with the current time
        """
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('SELECT NOW()')
            time=cursor.fetchone()[0]
            return time
        except Exception as e:
            print('couldnt get current time ' + str(e))

    def get_StudentProjectClicks(self,studentID):
        """
        gets the 50 most recent clicks of a certain student
        :param studentID: the student id
        :return: a list of project id's
        """
        try:
            cursor=self.dbconnect.get_cursor()
            cursor.execute('execute getStudentProjectClicks(%s)',(str(studentID),))
            projs=list()
            for row in cursor:
                projs.append(row)
            return  projs
        except Exception as e:
            print('couldnt get student project clicks '+str(e))
            return None