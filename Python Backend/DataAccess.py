from Bookmark import *
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
    this function as been shelved
    """
    # def manualDataHandling(self):
    #     while(True):
    #         inp = input("geeft input")
    #         if (inp == "makedoc"):
    #             inp = input("geeft uw document")
    #             self.add_document(Document(inp))
    #         elif (inp == "getdoc"):
    #             temp = self.get_documents()
    #             for doc in temp:
    #                 print(doc)
    #         elif (inp == "getgroup"):
    #             temp = self.get_researchGroups()
    #             for i in temp:
    #                 print(i)
    #         elif (inp == "makegroup"):
    #             name = input("give name")
    #             abb = input("give abbreviation")
    #             disc = input("give discipline")
    #             active = input("give active") == "True"
    #             adress = input("give adress")
    #             tel = input("give number")
    #             desc = input("give decription")
    #             temp = ResearchGroup(name, abb, disc, active, adress, tel, desc)
    #             self.add_researchGroup(temp)
    #         elif(inp=="getmployee"):
    #             temp=self.get_employees()
    #             for i in temp:
    #                 print(i)

    def get_documents(self):
        cursor=self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents=list()
        for row in cursor:
            document=Document(row[0],row[1],row[2])
            documents.append(document)
        return documents

    def get_document(self,id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document WHERE documentID=%s', (str(id) ))
        row= cursor.fetchone()
        return Document(row[0],row[1],row[2])

    #returns the document id of the added document
    def add_document(self, doc):
        cursor = self.dbconnect.get_cursor()
        try:
            id=None
            if(doc.ID!=None):
                # cursor.execute('INSERT INTO document VALUES(%s,%s,%s)', (doc.ID,doc.language,doc.text,))
                id=doc.ID

            else:
                cursor.execute('INSERT INTO document VALUES(default ,%s,%s)', ( doc.language, doc.text,))
                cursor.execute('SELECT LASTVAL()')
                id = cursor.fetchone()[0]
                doc.ID=id
            # get id and return updated object
            self.dbconnect.commit()
            return id
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!')


    def get_researchgroupDescriptions(self,groupid):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from groupDescription where groupID=%s', (str(groupid)))
        desc = list()
        for row in cursor:
            desc.append(self.get_document(row[1]))
        return desc

    def add_researchGroupDescription(self,document,groupid):
        cursor = self.dbconnect.get_cursor()
        try:
            docid=self.add_document(document)
            cursor.execute('INSERT INTO groupDescription values(%s,%s)',
                           (str(groupid),str(docid)))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroupdescription!')

    def get_researchGroups(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from researchGroup')
        rgroups=list()
        for row in cursor:
            rgroup=ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6],None)
            rgroup.desc=self.get_researchgroupDescriptions(rgroup.ID)
            rgroups.append(rgroup)
        return rgroups

    def get_researchGroupOnName(self, name):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGorup WHERE name=%s', (name))
        row = cursor.fetchone()
        rgroup= ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6],None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        return rgroup

    def get_researchGroupOnID(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGorup WHERE groupID=%s', (id))
        row = cursor.fetchone()
        rgroup= ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6],None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        return rgroup


    def add_researchGroup(self,group):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO researchGroup values(default ,%s,%s,%s,%s,%s,%s)',
                           (group.name,group.abbreviation,group.discipline,group.active,group.address,group.telNr))
            cursor.execute('SELECT LASTVAL()')
            gid = cursor.fetchone()[0]
            group.ID=gid
            for i in group.desc:
                self.add_researchGroupDescription(i,gid)
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroup!')


    def get_employees(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employee')
        employees= list()
        for row in cursor:
            employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7])
            employees.append(employee)
        return employees

    def get_employee(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE employeeID=%s ', (id))
        row = cursor.fetchone()
        return Employee(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7])

    def add_employee(self,empl):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employee values(default,%s,%s,%s,%s,%s,%s,%s)',
                           (empl.name,empl.email,empl.office,empl.researchGruoup,empl.title,empl.internOrExtern,empl.active))
            cursor.execute('SELECT LASTVAL()')
            eid = cursor.fetchone()[0]
            empl.Id=eid
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save Employee!')

    def get_projectDocuments(self, projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectDocument where projectID=%s', (str(projectID)))
        desc = list()
        for row in cursor:
            desc.append(self.get_document(row[1]))
        return desc

    def add_projectDocument(self, document, projectID):
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.add_document(document)
            cursor.execute('INSERT INTO projectDocument values(%s,%s)',
                           (str(projectID), str(docid)))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectdocument!')

    def get_projects(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from project')
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],None)
            project.desc=self.get_projectDocuments(str(project.ID))
            projects.append(project)
        return projects

    def get_project(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE projectID=%s ', (ID))
        row = cursor.fetchone()
        return Project(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],row[8])


    def filter_projects(self, searchQuery, type, discipline, researchGroup, status):
        cursor = self.dbconnect.get_cursor()

        ### Default Values ###
        # searchQuery = ''
        # type = ""
        # researchGroup = ""
        # discipline = ""
        # status = 0

        typeDefined = "%(typeQ)s"
        researchGroupDefined = "%(researchGroupQ)s"
        disciplineDefined = "%(disciplineQ)s"

        if (type == ""):
            typeDefined = "type "
        if (researchGroup == ""):
            researchGroupDefined = "name "
        if (discipline == ""):
            disciplineDefined = "discipline "

        if (status == 1):
            sql = "SELECT * FROM project INNER JOIN researchGroup ON researchGroup.groupID=project.researchGroup " \
                  "WHERE title LIKE %(searchQueryQ)s " \
                  "AND type = " + typeDefined + \
                  "AND name = " + researchGroupDefined + \
                  "AND discipline = " + disciplineDefined + \
                  "AND ((SELECT COUNT(student) FROM project INNER JOIN projectRegistration ON project.projectID=projectRegistration.project) < maxStudents) "
        elif (status == 2):
            sql = "SELECT * FROM project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup " \
                  "WHERE title LIKE %(searchQueryQ)s " \
                  "AND type = " + typeDefined + \
                  "AND name = " + researchGroupDefined + \
                  "AND discipline = " + disciplineDefined + \
                  "AND ((SELECT COUNT(student) FROM project INNER JOIN projectRegistration ON project.projectID=projectRegistration.project) >= maxStudents) "
        else:
            sql = "SELECT * FROM project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup " \
                  "WHERE title LIKE %(searchQueryQ)s " \
                  "AND type = " + typeDefined + \
                  "AND name = " + researchGroupDefined + \
                  "AND discipline = " + disciplineDefined

        cursor.execute( sql, dict(searchQueryQ = '%' +  searchQuery +'%',typeQ = type, researchGroupQ = researchGroup, disciplineQ = discipline ))

        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],None)
            project.desc=self.get_projectDocuments(str(project.ID))
            projects.append(project)
        return projects

    def add_project(self,proj):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO project values(default,%s,%s,%s,%s,%s,%s,%s)',
                           (proj.title, str(proj.maxStudents), proj.researchGroup, proj.activeYear,
                            proj.type, proj.tag, proj.projectId,proj.relatedProject))
            for i in proj.desc:
                self.add_projectDocument(i,proj.projectId)
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
            session = Session(row[0], row[1], row[2], row[3], row[4],row[5])
            sessions.append(session)
        return sessions

    def get_session(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE sessionID=%s ', (ID))
        row = cursor.fetchone()
        return Session(row[0], row[1], row[2], row[3], row[4],row[5])

    def add_session(self,ses):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO session values(%s,%s,%s,%s,%s,%s)',
                           (str(ses.sessionId), ses.startTime, ses.searchWord, ses.searchWordTime, ses.clickedProject, ses.clickedProjectTime))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save session!')

    #returns all the bookmarks of the student
    def get_studentBookmarks(self,studentId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where student=%s',(str(studentId)))
        bookmarks = list()
        for row in cursor:
            bookmarker = Bookmark(row[0], row[1])
            bookmarks.append(bookmarker)
        return bookmarks

    #return the projects of all the bookmarks a student has
    def get_studentBookmarkProject(self,studentId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where student=%s', (str(studentId)))
        projects = list()
        for row in cursor:
            projects.append(self.get_project(row[0]))
        return projects

    #returns all bookmarks to a certain project
    def get_projectBookmarks(self,projectId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s', (str(projectId)))
        bookmarks = list()
        for row in cursor:
            bookmark = bookmark(row[0], row[1])
            bookmarks.append(bookmark)
        return bookmarks

    def add_bookmark(self,projectId,studentId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s and student=%s', (str(projectId),str(studentId)))
        if cursor.rowcount==0:
            cursor.execute('insert into bookmark values(%s,%s)', (str(projectId),str(studentId)))

    def get_students(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from student')
        students = list()
        for row in cursor:
            student = Student(row[0], row[1], row[2], None)
            student.likedProject=self.get_studentBookmarkProject(student.studentID)
            students.append(student)
        return students

    def get_student(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE studentID=%s ', (str(ID)))
        row = cursor.fetchone()
        stu= Student(row[0], row[1], row[2], None)
        stu.likedProject = self.get_studentBookmarkProject(stu.studentID)
        return stu

    def add_student(self, stu):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO student values(%s,%s,%s)',
                           (str(stu.studentId), stu.name, stu.session))
            for i in stu.likedProject:
                self.add_bookmark(i.ID,stu.studentId)

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
                           (str(pr.project), pr.status, str(pr.student)))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save project registration!')