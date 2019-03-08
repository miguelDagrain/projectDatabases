from Bookmark import *
from Document import *
from ResearchGroup import *
from Employee import *
from Project import *
from ProjectRegistration import *
from Session import *
from Student import *
from Attachment import *


class DataAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_documents(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents=list()
        for row in cursor:
            document=Document(row[0],row[1],row[2])
            cursorAttachment = self.dbconnect.get_cursor()
            cursorAttachment.execute('select * from attachment where %s=doc',(str(document.ID)))
            for att in cursorAttachment:
                document.attachment.append(Attachment(att[0],att[1]))
            documents.append(document)
        return documents

    def get_document(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document WHERE documentID=%s', (str(id) ))
        row= cursor.fetchone()
        document=Document(row[0],row[1],row[2])
        cursorAttachment = self.dbconnect.get_cursor()
        cursorAttachment.execute('select * from attachment where %s=doc',(str(document.ID)))
        for att in cursorAttachment:
            document.attachment.append(Attachment(att[0], att[1]))

    def add_attachment(self,attachment):
        try:
            cursor =self.dbconnect.get_cursor()
            cursor.execute('select * from attachment where doc=%s and attachment=%s',(str(attachment.docid),attachment.content))
            if(cursor.rowcount==0):
                cursor.execute('insert into attachment values(%s,%s)',(str(attachment.docid),attachment.content))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save attachment!')

    # returns the document id of the added document
    def add_document(self, doc):
        cursor = self.dbconnect.get_cursor()
        try:
            id = None
            if (doc.ID != None):
                # cursor.execute('INSERT INTO document VALUES(%s,%s,%s)', (doc.ID,doc.language,doc.text,))
                id = doc.ID

            else:
                cursor.execute('INSERT INTO document VALUES(default ,%s,%s)', (doc.language, doc.text,))
                cursor.execute('SELECT LASTVAL()')
                id = cursor.fetchone()[0]
                doc.ID=id
                for att in doc.attachment:
                    att.docid=id
                    self.add_attachment(att)
            # get id and return updated object
            self.dbconnect.commit()
            return id
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!')

    def get_researchgroupDescriptions(self, groupid):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from groupDescription where groupID=%s', (str(groupid)))
        desc = list()
        for row in cursor:
            desc.append(self.get_document(row[1]))
        return desc

    def add_researchGroupDescription(self, document, groupid):
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.add_document(document)
            cursor.execute('INSERT INTO groupDescription values(%s,%s)',
                           (str(groupid), str(docid)))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroupdescription!')

    def get_researchGroups(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from researchGroup')
        rgroups = list()
        for row in cursor:
            rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
            rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
            newcursor=self.dbconnect.get_cursor()
            newcursor.execute('select * from contactPerson where rgroup=%s', (str(rgroup.ID)))
            if (newcursor.rowcount > 0):
                rgroup.contactID = newcursor.fetchone()[0]
            rgroups.append(rgroup)
        return rgroups

    def get_researchGroupOnName(self, name):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGorup WHERE name=%s', (name))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s',(str(rgroup.ID)))
        if(cursor.rowcount>0):
            rgroup.contactID=cursor[0][0]
        return rgroup

    def get_researchGroupOnID(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGroup WHERE groupID=%s', (id))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s', (str(rgroup.ID)))
        if (cursor.rowcount > 0):
            rgroup.contactID = row[0][0]
        return rgroup

    def checkContactPerson(self,eid,groupID):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('SELECT * FROM contactPerson WHERE groupID=%s', (groupID))
            if(cursor.rowcount==0):
                cursor.execute('insert into contactperson values(%s,%s)',(eid,groupID))
            else:
                if(cursor[0][0]!=eid):
                    cursor.execute('update contactPerson SET employee=%s where rgroup=%s',(eid,groupID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to check contactperson !')
    def add_researchGroup(self, group):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO researchGroup values(default ,%s,%s,%s,%s,%s,%s)',
                           (group.name, group.abbreviation, group.discipline, group.active, group.address, group.telNr))
            cursor.execute('SELECT LASTVAL()')
            gid = cursor.fetchone()[0]
            group.ID = gid
            if(group.contactID!=None):
                self.checkContactPerson(group.contactId,group.ID)
            for i in group.desc:
                self.add_researchGroupDescription(i, gid)
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroup!')

    def get_employees(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employee')
        employees = list()
        for row in cursor:
            employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            employees.append(employee)
        return employees

    def get_employee(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE employeeID=%s ', (id))
        row = cursor.fetchone()
        return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    def add_employee(self, empl):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employee values(default,%s,%s,%s,%s,%s,%s,%s)',
                           (empl.name, empl.email, empl.office, empl.researchGruoup, empl.title, empl.internOrExtern,
                            empl.active))
            cursor.execute('SELECT LASTVAL()')
            eid = cursor.fetchone()[0]
            empl.Id = eid
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

    def get_projectYears(self,projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectYearConnection where projectID=%s',(str(projectID)))
        years = list()
        for i in cursor:
            years.append(i[0])
        return years

    def add_projectYears(self,projectId, year):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectYear where year=%s',(str(year)))
            if(cursor.rowcount==0):
                cursor.execute('insert into projectYear values(%s)',(str(year)))
            cursor.execute('select * from projectYearConnection where year=%s and projectID=%s',(year,projectId))
            if(cursor.rowcount==0):
                cursor.execute('insert into projectYearConnection values(%s,%s)',(year,projectId))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectYear!')

    def get_projectTypes(self, projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectYearConnection where projectID=%s', (str(projectID)))
        types = list()
        for i in cursor:
            types.append(i[0])
        return types

    def add_projectType(self, projectId, type):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectType where year=%s', (str(type)))
            if (cursor.rowcount == 0):
                cursor.execute('insert into projectType values(%s)', (str(type)))
            cursor.execute('select * from projectTypeConnection where type=%s and projectID=%s', (type, projectId))
            if (cursor.rowcount == 0):
                cursor.execute('insert into projectTypeConnection values(%s,%s)', (type, projectId))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectType!')

    def get_projectPromotors(self,projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectPromotor where project=%s',(str(projectID)))
        proms=list()
        for row in cursor:
            proms.append(row[0])
        return proms

    def add_projectPromotor(self,projectID,employeeId):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectPromoter where employee=%s and project=%s',employeeId,projectID)
            if(cursor.rowcount==0):
                cursor.execute('insert into projectPromotor values(%s,%s)',(employeeId,projectID))
        except:
            self.dbconnect.rollback()
            print("unable to safe promotor")

    def get_projectTags(self,projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectTag where project=%s', (str(projectID)))
        tags = list()
        for row in cursor:
            tags.append(row[0])
        return tags

    def add_projectTag(self,projectID,tag):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectTag where tag=%s and project=%s', tag, str(projectID))
            if (cursor.rowcount == 0):
                cursor.execute('insert into projectTag values(%s,%s)', (tag, str(projectID)))
        except:
            self.dbconnect.rollback()
            print("unable to save tag")

    def get_projectRelations(self,projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRelation where project1=%s', (str(projectID)))
        related = list()
        for row in cursor:
            related.append(row[1])
        cursor.execute('select * from projectRelation where project2=%s', (str(projectID)))
        for row in cursor:
            if row[0] not in related:
                related.append(row[0])
        return related

    def add_projectRelation(self,project1ID,project2ID):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from  projectRelation where project1=%s and project2=%s',(str(project1ID), str(project2ID)))
            if (cursor.rowcount == 0):
                cursor.execute('insert into projectRelation values(%s,%s)', (str(project1ID), str(project2ID)))
        except:
            self.dbconnect.rollback()
            print("unable to save tag")

    def get_projects(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from project')
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3],row[4])
            project.desc = self.get_projectDocuments(str(project.ID))
            project.activeYear = self.get_projectYears(project.ID)
            project.promotor=self.get_projectPromotors(project.ID)
            project.tag=self.get_projectTags(project.ID)
            project.relatedProject=self.get_projectRelations(project.ID)
            projects.append(project)

        return projects

    def get_project(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM project WHERE projectID=%s ', (str(ID)))
        row = cursor.fetchone()
        project=Project(row[0], row[1], row[2], row[3],row[4])
        project.desc = self.get_projectDocuments(str(project.ID))
        project.activeYear = self.get_projectYears(project.ID)
        project.promotor = self.get_projectPromotors(project.ID)
        project.tag = self.get_projectTags(project.ID)
        project.relatedProject = self.get_projectRelations(project.ID)
        return project

    def filter_projects(self, searchQuery="", type="", discipline=None, researchGroup="", status=0):
        cursor = self.dbconnect.get_cursor()


        sql = "SELECT * FROM project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup " \
              "WHERE p.title LIKE %(searchQueryQ)s "

        if (researchGroup != ""):
            sql += "AND name = %(researchGroupQ)s"
        if (type != ""):
            sql += "AND type = %(typeQ)s"

        discipline1 = ""
        discipline2 = ""
        discipline3 = ""

        if (discipline != None):

            if (len(discipline) >= 1):
                discipline1 = discipline[0]
                sql += "AND (discipline = %(disciplineQ1)s"
            if (len(discipline) >= 2):
                discipline2 = discipline[1]
                sql += "OR discipline = %(disciplineQ2)s"
            if (len(discipline) == 3):
                discipline3 = discipline[2]
                sql += "OR discipline = %(disciplineQ3)s"

            sql += ")"

        #gemeenschappelijke sql uit de if else structuur gehaald.
        if (status == 1):

            sql +="AND ((SELECT COUNT(student) FROM project INNER JOIN projectRegistration ON project.projectID=projectRegistration.project) < maxStudents) "

        elif (status == 2):

            sql += "AND ((SELECT COUNT(student) FROM project INNER JOIN projectRegistration ON project.projectID=projectRegistration.project) >= maxStudents) "


        cursor.execute(sql, dict(searchQueryQ="%"+ searchQuery +"%", researchGroupQ=researchGroup,
                                 disciplineQ1=discipline1, disciplineQ2=discipline2, disciplineQ3=discipline3))

        projects= list()
        for row in cursor:
            project = self.get_project(row[0])
            projects.append(project)
        return projects



    def add_project(self, proj):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO project values(default,%s,%s,%s,%s)',
                (proj.title, str(proj.maxStudents),proj.active, proj.researchGroup))
            cursor.execute('SELECT LASTVAL()')
            gid = cursor.fetchone()[0]
            proj.ID = gid
            for i in proj.desc:
                self.add_projectDocument(i, proj.projectId)
            for i in proj.activeYear:
                self.add_projectYears(gid,i)
            for i in proj.type:
                self.add_projectType(gid,i)
            for i in proj.tag:
                self.add_projectTag(gid,i)
            for i  in proj.relatedProject:
                self.add_projectRelation(gid,i)
            for i in proj.promotor:
                self.add_projectPromotor(gid,i)
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save project!')



    # returns all the bookmarks of the student
    def get_studentBookmarks(self, studentId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where student=%s', (str(studentId)))
        bookmarks = list()
        for row in cursor:
            bookmarker = Bookmark(row[0], row[1])
            bookmarks.append(bookmarker)
        return bookmarks

    # return the projects of all the bookmarks a student has
    def get_studentBookmarkProject(self, studentId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where student=%s', (str(studentId)))
        projects = list()
        for row in cursor:
            projects.append(self.get_project(row[0]))
        return projects

    # returns all bookmarks to a certain project
    def get_projectBookmarks(self, projectId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s', (str(projectId)))
        bookmarks = list()
        for row in cursor:
            bookmark = bookmark(row[0], row[1])
            bookmarks.append(bookmark)
        return bookmarks

    def add_bookmark(self, projectId, studentId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s and student=%s', (str(projectId), str(studentId)))
        if cursor.rowcount == 0:
            cursor.execute('insert into bookmark values(%s,%s)', (str(projectId), str(studentId)))

    def get_students(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from student')
        students = list()
        for row in cursor:
            student = Student(row[0], row[1])
            student.likedProject = self.get_studentBookmarkProject(student.studentID)
            students.append(student)
        return students

    def get_student(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE studentID=%s ', (str(ID)))
        row = cursor.fetchone()
        stu = Student(row[0], row[1])
        stu.likedProject = self.get_studentBookmarkProject(stu.studentID)
        return stu

    def add_student(self, stu):
        cursor = self.dbconnect.get_cursor()
        try:
            if(stu.studentId!=None):
                cursor.execute('INSERT INTO student values(%s,%s)',
                           (str(stu.studentId), stu.name))
            else:
                cursor.execute('INSERT INTO student values(default,%s)',
                               ( stu.name))
                cursor.execute('select lastval()')
                stu.studentId = cursor.fetchone()[0]
            for i in stu.likedProject:
                self.add_bookmark(i.ID, stu.studentId)

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

    def get_projectRegistrationsOnProject(self,projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration where project=%s',(projectID))
        prs = list()
        for row in cursor:
            pr = ProjectRegistration(row[0], row[1], row[2])
            prs.append(pr)
        return prs

    def get_projectRegistrationsOnStudent(self, studentID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration where student=%s', (studentID))
        prs = list()
        for row in cursor:
            pr = ProjectRegistration(row[0], row[1], row[2])
            prs.append(pr)
        return prs

    # this function is pretty useless at the moment because to get a single registration you need al the data from it
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

    def get_sessionSearches(self, sessionID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from sessionSearchQuery where sessionID=%s', (str(sessionID)))
        searchs = list()
        for row in cursor:
            searchs.append((row[1],row[2]))
        return searchs

    def add_sessionSearch(self, sessionId, search):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from sessionSearchQuery where sessionID=%s and term=%s and searchtTime=%s',(str(sessionId),search[0],search[1] ))
            if (cursor.rowcount == 0):
                cursor.execute('insert into sessionSearchQuery values(%s,%s,%s)', (str(sessionId),search[0],search[1] ))
        except:
            self.dbconnect.rollback()
            print("unable to save sessionsearch")

    def get_sessionProjectClicks(self, sessionID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from sessionProjectClick where sessionID=%s', (str(sessionID)))
        clicks = list()
        for row in cursor:
            clicks.append((row[1],row[2]))
        return clicks

    def add_sessionProjectClick(self, sessionId, click):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from sessionProjectClick where sessionID=%s and project=%s and searchtTime=%s',(str(sessionId),str(click[0]),click[1] ))
            if (cursor.rowcount == 0):
                cursor.execute('insert into sessionProjectClick values(%s,%s,%s)', (str(sessionId),str(click[0]),click[1] ) )
        except:
            self.dbconnect.rollback()
            print("unable to save sessionClick")

    def get_sessions(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from session')
        sessions = list()
        for row in cursor:
            session = Session(row[0], row[1], row[2], row[3])
            session.searchWords=self.get_sessionSearches(session.sessionId)
            session.clickedProjects=self.get_sessionProjectClicks(session.sessionId)
            sessions.append(session)
        return sessions

    def get_session(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE sessionID=%s ', (ID))
        row = cursor.fetchone()
        session= Session(row[0], row[1], row[2], row[3])
        session.searchWords = self.get_sessionSearches(session.sessionId)
        session.clickedProjects = self.get_sessionProjectClicks(session.sessionId)
        return session

    def add_session(self, ses):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO session values(%s,%s,%s,%s)',
                           (str(ses.sessionId), str(ses.studentId),ses.startTime,ses.startDate))

            for i in ses.searchWords:
                self.add_sessionSearch(ses.sessionId,i)
            for i in ses.clickedProjects:
                self.add_sessionProjectClick(ses.sessionId,i)
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save session!')