from Document import *
from ResearchGroup import *
from Employee import *
from Project import *
from ProjectRegistration import *
from Session import *
from Student import *



class DataAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    """
    very ugly function to test teh database acces and possible manually handle data a little bit easier
    """
    def manualDataHandling(self):
        while(True):
            inp = input("geeft input")
            if (inp == "makedoc"):
                inp = input("geeft uw document")
                self.add_document(Document(inp))
            elif (inp == "getdoc"):
                temp = self.get_documents()
                for doc in temp:
                    print(doc)
            elif (inp == "getgroup"):
                temp = self.get_researchGroups()
                for i in temp:
                    print(i)
            elif (inp == "makegroup"):
                name = input("give name")
                abb = input("give abbreviation")
                disc = input("give discipline")
                active = input("give active") == "True"
                adress = input("give adress")
                tel = input("give number")
                desc = input("give decription")
                temp = ResearchGroup(name, abb, disc, active, adress, tel, desc)
                self.add_researchGroup(temp)
            elif(inp=="getmployee"):
                temp=self.get_employees()
                for i in temp:
                    print(i)

    def get_documents(self):
        cursor=self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents=list()
        for row in cursor:
            document=Document(row[0])
            documents.append(document)
        return documents

    def get_document(self,text):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document WHERE text=%s', (text ))
        row= cursor.fetchone()
        return Document(row[0])

    def add_document(self, doc):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO document VALUES(%s)', (doc.text,))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!')

    def get_researchGroups(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from researchGroup')
        rgroups=list()
        for row in cursor:
            rgroup=ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            rgroups.append(rgroup)
        return rgroups

    def get_researchGroup(self, name,abbr):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGorup WHERE name=%s  and abbreviation=%s', (name,abbr))
        row = cursor.fetchone()
        return ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6])


    def add_researchGroup(self,group):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO researchGroup values(%s,%s,%s,%s,%s,%s,%s)',
                           (group.name,group.abbreviation,group.discipline,group.active,group.address,group.telNr,group.desc))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroup!')


    def get_employees(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employee')
        employees= list()
        for row in cursor:
            employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5])
            employees.append(employee)
        return employees

    def get_employee(self, email):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE email=%s ', (email))
        row = cursor.fetchone()
        return Employee(row[0], row[1], row[2], row[3], row[4], row[5])

    def add_employee(self,empl):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employee values(%s,%s,%s,%s,%s,%s)',
                           (empl.email,empl.office,empl.researchGruoup,empl.title,empl.internOrExtern,empl.active))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save Employee!')

    def get_projects(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from project')
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],row[8])
            projects.append(project)
        return projects

    def get_project(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE projectID=%s ', (ID))
        row = cursor.fetchone()
        return Project(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],row[8])

    def add_project(self,proj):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO project values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (proj.title, proj.maxStudents, proj.description, proj.researchGroup, proj.activeYear,
                            proj.type, proj.tag, proj.projectId,proj.relatedProject))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save project!')

    def get_sessions(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from session')
        sessions = list()
        for row in cursor:
            session = Session(row[0], row[1], row[2], row[3], row[4])
            sessions.append(session)
        return sessions

    def get_session(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE sessionID=%s ', (ID))
        row = cursor.fetchone()
        return Session(row[0], row[1], row[2], row[3], row[4])

    def add_session(self,ses):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO session values(%s,%s,%s,%s,%s)',
                           ( ses.sessionId, ses.startTime, ses.searchWordTime, ses.clickedProject, ses.clickedProjectTime))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save session!')

    def get_students(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from student')
        students = list()
        for row in cursor:
            student = Student(row[0], row[1], row[2], row[3])
            students.append(student)
        return students

    def get_student(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE studentID=%s ', (ID))
        row = cursor.fetchone()
        return Student(row[0], row[1], row[2], row[3])

    def add_student(self, stu):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO student values(%s,%s,%s,%s)',
                           (stu.name, stu.studentId, stu.likedProject, stu.session))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save session!')

    def get_projectRegistrations(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration')
        prs = list()
        for row in cursor:
            pr = ProjectRegistration(row[0], row[1], row[2])
            prs.append(pr)
        return prs

    #this function is pretty useless at the moment because to get a single registration you need al the data from it
    # def get_projectRegistration(self):
    #     cursor = self.dbconnect.get_cursor()
    #     cursor.execute('select * from projectRegistration')
    #     prs = list()
    #     for row in cursor:
    #         pr = ProjectRegistration(row[0], row[1], row[2])
    #         prs.append(pr)
    #     return prs

    def add_projectRegistration(self, pr):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO projectRegistration values(%s,%s,%s)',
                           (pr.project, pr.status, pr.studentn))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save project registration!')