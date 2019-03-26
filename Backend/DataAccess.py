class DocumentAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_documents(self):
        from Document import Document
        from Attachment import Attachment
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents = list()
        for row in cursor:
            document = Document(row[0], row[1], row[2])
            cursorAttachment = self.dbconnect.get_cursor()
            cursorAttachment.execute('select * from attachment where %s=doc', (str(document.ID)))
            for att in cursorAttachment:
                document.attachment.append(Attachment(att[0], att[1]))
            documents.append(document)
        return documents

    def get_document(self, id):
        from Document import Document
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document WHERE documentID=%s', (str(id)))
        row = cursor.fetchone()
        document = Document(row[0], row[1], row[2])
        cursorAttachment = self.dbconnect.get_cursor()
        cursorAttachment.execute('select * from attachment where %s=doc', (str(document.ID)))
        for att in cursorAttachment:
            document.attachment.append(att[1])
        return document

    def add_attachment(self, documentID, attachment):
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('select * from attachment where doc=%s and attachment=%s',
                           (str(documentID), str(attachment)))
            if cursor.rowcount == 0:
                cursor.execute('insert into attachment values(%s,%s)', (str(documentID), str(attachment)))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save attachment!')

    # returns the document id of the added document
    def add_document(self, doc):
        cursor = self.dbconnect.get_cursor()
        try:
            id = None
            if doc.ID is not None:
                # cursor.execute('INSERT INTO document VALUES(%s,%s,%s)', (doc.ID,doc.language,doc.text,))
                id = doc.ID

            else:
                cursor.execute('INSERT INTO document VALUES(default ,%s,%s)', (doc.language, str(doc.text)))
                cursor.execute('SELECT LASTVAL()')
                id = cursor.fetchone()[0]
                doc.ID = id
                for att in doc.attachment:
                    att.docid = id
                    self.add_attachment(att)
            # get id and return updated object
            self.dbconnect.commit()
            return id
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!')

    def change_Document(self, document):
        try:
            if document.ID is not None:
                cursor = self.dbconnect.get_cursor()
                cursor.execute('select * from document where documentID=%s', (str(document.ID)))
                if cursor.rowcount == 0:
                    raise Exception('no document with that ID found')
                cursor.execute('update document set lang= %s, content= %s where documentID=%s',
                               (document.language, document.text, str(document.ID)))

                cursor.execute('delete from attachment where doc=%s', (str(document.ID)))
                for i in document.attachment:
                    self.add_attachment(document.ID, i)
                self.dbconnect.commit()

            else:
                raise Exception('Document doesnt have ID')
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to change document!')


class ResearchGroupAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect
        self.doc = DocumentAccess(self.dbconnect)

    def get_researchgroupDescriptions(self, groupid):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from groupDescription where groupID=%s', (str(groupid)))
        desc = list()
        for row in cursor:
            desc.append(self.doc.get_document(row[1]))
        return desc

    def add_researchGroupDescription(self, document, groupid):
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.doc.add_document(document)
            cursor.execute('INSERT INTO groupDescription values(%s,%s)',
                           (str(groupid), str(docid)))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroupdescription!')

    def get_researchGroups(self):
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from researchGroup')
        rgroups = list()
        for row in cursor:
            rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
            rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
            newcursor = self.dbconnect.get_cursor()
            newcursor.execute('select * from contactPerson where rgroup=%s', (str(rgroup.ID)))
            if newcursor.rowcount > 0:
                rgroup.contactID = newcursor.fetchone()[0]
            rgroups.append(rgroup)
        return rgroups

    def get_researchGroupOnName(self, name):
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGroup WHERE name=%s', (name))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s', (str(rgroup.ID)))
        if cursor.rowcount > 0:
            rgroup.contactID = cursor.fetchone()[0]
        return rgroup

    def get_researchGroupOnID(self, id):
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGroup WHERE groupID=%s', (str(id)))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s', (str(rgroup.ID)))
        if cursor.rowcount > 0:
            rgroup.contactID = cursor.fetchone()[0]
        return rgroup

    def remove_researchGroup(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM researchGroup WHERE groupID=%s', (str(id)))
        self.dbconnect.commit()
        return

    def checkContactPerson(self, eid, groupID):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('SELECT * FROM contactPerson WHERE rgroup=%s', (str(groupID)))
            if cursor.rowcount == 0:
                cursor.execute('insert into contactperson values(%s,%s)', (str(eid), str(groupID)))
            else:
                if (cursor.fetchone()[0] != eid):
                    # waarom zegt pycharm hier constant dat hem '=' verwacht terwijl dat er staat ???
                    cursor.execute('update contactPerson set employee= %s where rgroup=%s', (str(eid), str(groupID)))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to check contactperson !')

    def add_researchGroup(self, group):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO researchGroup values(default ,%s,%s,%s,%s,%s,%s)',
                           (group.name, group.abbreviation, group.discipline, group.active, group.address,
                            str(group.telNr)))
            cursor.execute('SELECT LASTVAL()')
            gid = cursor.fetchone()[0]
            group.ID = gid
            if group.contactID != None:
                self.checkContactPerson(group.contactId, group.ID)
            for i in group.desc:
                self.add_researchGroupDescription(i, gid)
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroup!')

    def change_researchGroup(self, group):
        cursor = self.dbconnect.get_cursor()
        try:
            if group.ID == None:
                raise Exception('no id given')
            cursor.execute('select * from researchgroup where groupID=%s', (str(group.ID)))
            if cursor.rowcount == 0:
                raise Exception('no researchGroup found with that id')
            cursor.execute(
                'update researchGroup set name= %s,abbreviation= %s,discipline= %s,active= %s,address= %s,telNr= %s where groupId=%s',
                (group.name, group.abbreviation, group.discipline, group.active, group.address, str(group.telNr)),
                str(group.ID))
            cursor.execute('delete from groupDescription where groupID=%s', str(group.ID))
            for i in group.desc:
                self.add_researchGroupDescription(i, str(group.ID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change researchGroup')


class EmployeeAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_employees(self):
        from Employee import Employee
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employee')

        employees = list()
        for row in cursor:
            employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            employees.append(employee)
        return employees

    def get_employee(self, id):
        from Employee import Employee
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE employeeID=%s ', (str(id)))
        row = cursor.fetchone()
        return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    def add_employee(self, empl):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employee values(default,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (empl.name, empl.email, empl.office, empl.research_group.ID, empl.title, empl.internOrExtern,
                            empl.active, empl.promotor))
            cursor.execute('SELECT LASTVAL()')
            eid = cursor.fetchone()[0]
            empl.Id = eid
            # get id and return updated object
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to save Employee!\n(%s)' % (error))

    def remove_employee(self, id):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM employee WHERE employeeID=%s', (str(id)))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to remove Employee!\n(%s)' % (error))

    def filter_employees(self, searchQuery="", researchGroup="", promotor=0, ):
        from Employee import Employee
        cursor = self.dbconnect.get_cursor()

        sql = 'select * from employee e INNER JOIN researchGroup r ON r.groupID=e.researchGroup WHERE ' \
              'e.name LIKE %(searchQueryQ)s'

        if researchGroup != "":
            sql += "AND r.name = %(researchGroupQ)s"

        if promotor == 1:
            sql += 'AND e.promotor = TRUE'
        if promotor == 2:
            sql += 'AND e.promotor = FALSE'

        cursor.execute(sql, dict(searchQueryQ="%" + searchQuery + "%", researchGroupQ=researchGroup))
        employees = list()
        for row in cursor:
            employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            employees.append(employee)
        return employees

    def add_employeeRole(self, id, role):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employeeRoles values(%s,%s)',
                           (str(id), role))
            # get id and return updated object
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to save EmployeeRole!\n(%s)' % (error))

    def get_employeeRoles(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employeeRoles where employee=%s', (str(id)))
        roles = list()
        for row in cursor:
            roles.append(row[1])
        return roles

    def change_employee(self, employee):
        cursor = self.dbconnect.get_cursor()
        try:
            if employee.ID == None:
                raise Exception('no id given')
            cursor.execute('select * from employee where employeeID=%s', (str(employee.ID)))
            if cursor.rowcount == 0:
                raise Exception('no employee found with that id')
            cursor.execute(
                'update employee set name= %s,email= %s,office= %s,researchgroup= %s,title= %s,INTernORextern= %s,active= %s,promotor= %s where employeeID=%s',
                (employee.name, employee.email, employee.office, str(employee.research_group), employee.title,
                 employee.internOrExtern, employee.active, str(employee.promotor), str(employee.ID)))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change employee')


class ProjectAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect
        self.doc = DocumentAccess(self.dbconnect)

    def get_projectDocuments(self, projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectDocument where projectID=%s', (str(projectID)))
        desc = list()
        for row in cursor:
            desc.append(self.doc.get_document(row[1]))
        return desc

    def add_projectDocument(self, projectID, document):
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.doc.add_document(document)
            cursor.execute('INSERT INTO projectDocument values(%s,%s)',
                           (str(projectID), str(docid)))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectdocument!')

    def get_projectYears(self, projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectYearConnection where projectID=%s', (str(projectID)))
        years = list()
        for i in cursor:
            years.append(i[0])
        return years

    def add_projectYears(self, projectId, year):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectYear where year=%s', (str(year)))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectYear values(%s)', (str(year)))
            cursor.execute('select * from projectYearConnection where year=%s and projectID=%s',
                           (str(year), str(projectId)))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectYearConnection values(%s,%s)', (str(year), str(projectId)))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectYear!')

    def get_typesFromProject(self, projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectYearConnection where projectID=%s', (str(projectID)))
        types = list()
        for i in cursor:
            types.append(i[0])
        return types

    def add_projectTypeConnection(self, projectId, type):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectTypeConnection where type=%s and projectID=%s',
                           (str(type), str(projectId)))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectTypeConnection values(%s,%s)', (str(type), str(projectId)))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectType!')

    def get_projectPromotors(self, projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectPromotor where project=%s', (str(projectID)))
        proms = list()
        for row in cursor:
            proms.append(row[0])
        return proms

    def add_projectPromotor(self, projectID, employeeId):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectPromotor where employee=%s and project=%s',
                           (str(employeeId), str(projectID)))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectPromotor values(%s,%s)', (str(employeeId), str(projectID)))
        except:
            self.dbconnect.rollback()
            print("unable to safe promotor")

    def get_projectTags(self, projectID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectTag where project=%s', (str(projectID)))
        tags = list()
        for row in cursor:
            tags.append(row[0])
        return tags

    def add_projectTag(self, projectID, tag):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectTag where tag=%s and project=%s', tag, str(projectID))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectTag values(%s,%s)', (tag, str(projectID)))
        except:
            self.dbconnect.rollback()
            print("unable to save tag")

    def get_projectRelations(self, projectID):
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

    def add_projectRelation(self, project1ID, project2ID):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from  projectRelation where project1=%s and project2=%s',
                           (str(project1ID), str(project2ID)))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectRelation values(%s,%s)', (str(project1ID), str(project2ID)))
        except:
            self.dbconnect.rollback()
            print("unable to save tag")

    def get_projects(self):
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from project')
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3], row[4])
            project.desc = self.get_projectDocuments(str(project.ID))
            project.activeYear = self.get_projectYears(project.ID)
            project.promotor = self.get_projectPromotors(project.ID)
            project.tag = self.get_projectTags(project.ID)
            project.relatedProject = self.get_projectRelations(project.ID)
            projects.append(project)

        return projects

    def get_project(self, ID):
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM project WHERE projectID=%s ', (str(ID)))
        row = cursor.fetchone()
        project = Project(row[0], row[1], row[2], row[3], row[4])
        project.desc = self.get_projectDocuments(str(project.ID))
        project.activeYear = self.get_projectYears(project.ID)
        project.promotor = self.get_projectPromotors(project.ID)
        project.tag = self.get_projectTags(project.ID)
        project.relatedProject = self.get_projectRelations(project.ID)
        return project

    def remove_project(self, ID):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM project WHERE projectID=%s', (str(ID)))
        self.dbconnect.commit()
        return

    def get_project_filter_data(self):
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        sql = "SELECT p.projectid, title, maxstudents, p.active, name, discipline, type FROM (project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup)" \
              "INNER JOIN projectTypeConnection ON p.projectid=projectTypeConnection.projectID"

        sql = "SELECT p.projectid, title, maxstudents, p.active, name, discipline, type, (" \
              "SELECT COUNT(*) FROM projectregistration pr WHERE pr.project=p.projectid) as cnt " \
              "FROM (project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup)" \
              "INNER JOIN projectTypeConnection ON p.projectid=projectTypeConnection.projectID"

        cursor.execute(sql);
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3], row[4])
            project.type = row[6]
            project.desc = self.get_projectDocuments(str(project.ID))
            project.discipline = row[5]
            project.registeredStudents = row[7]
            projects.append(project)
        return projects

    def filter_projects(self, searchQuery="", type="", discipline=None, researchGroup="", status=0):
        cursor = self.dbconnect.get_cursor()

        sql = "SELECT * FROM project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup " \
              "WHERE p.title LIKE %(searchQueryQ)s "

        if researchGroup != "":
            sql += "AND name = %(researchGroupQ)s "
        # hier is een fout typeQ wordt nooit vervangen
        # todo: implementeren van type in sql.
        # if (type != ""):
        #     sql += "AND type = %(typeQ)s "

        disciplineValue = ""

        if discipline is not None:

            sql += "AND discipline IN ( "

            for iterDiscipline in discipline:
                sql += "'" + iterDiscipline + "', "

            sql = sql[0:len(sql) - 2]
            sql += " ) "

        # gemeenschappelijke sql uit de if else structuur gehaald.
        if status == 1:

            sql += "AND ((SELECT COUNT(student) FROM project INNER JOIN projectRegistration ON project.projectID=projectRegistration.project) < maxStudents) "

        elif status == 2:

            sql += "AND ((SELECT COUNT(student) FROM project INNER JOIN projectRegistration ON project.projectID=projectRegistration.project) >= maxStudents) "

        cursor.execute(sql, dict(searchQueryQ="%" + searchQuery + "%", researchGroupQ=researchGroup))

        projects = list()
        for row in cursor:
            project = self.get_project(row[0])
            projects.append(project)
        return projects

    def add_project(self, proj):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO project values(default,%s,%s,%s,%s)',
                           (proj.title, str(proj.maxStudents), proj.active, proj.researchGroup))
            cursor.execute('SELECT LASTVAL()')
            gid = cursor.fetchone()[0]
            proj.ID = gid
            for i in proj.desc:
                self.add_projectDocument(proj.projectId, i)
            for i in proj.activeYear:
                self.add_projectYears(gid, i)
            for i in proj.type:
                self.add_projectTypeConnection(gid, i)
            for i in proj.tag:
                self.add_projectTag(gid, i)
            for i in proj.relatedProject:
                self.add_projectRelation(gid, i)
            for i in proj.promotor:
                self.add_projectPromotor(gid, i)
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save project!')

    def change_project(self, project):
        cursor = self.dbconnect.get_cursor()
        try:
            if project.ID == None:
                raise Exception('no id given')
            cursor.execute('select * from project where projectID=%s', (str(project.ID)))
            if cursor.rowcount == 0:
                raise Exception('no project found with that id')
            cursor.execute(
                'update project set title= %s,maxStudents= %s,active= %s,researchGroup= %s where projectID=%s',
                (project.title, str(project.maxStudents), project.active, str(project.researchGroup), str(project.ID)))

            cursor.execute('delete from projectYearConnection where projectID=%s', str(project.ID))
            for i in project.activeYear:
                self.add_projectYears(str(project.ID), i)

            cursor.execute('delete from projectTypeConnection where projectID=%s', str(project.ID))
            for i in project.type:
                self.add_projectTypeConnection(str(project.ID), i)

            cursor.execute('delete from projectPromotor where project=%s', str(project.ID))
            for i in project.promotor:
                self.add_projectPromotor(str(project.ID), i)

            cursor.execute('delete from projectTag where project=%s', str(project.ID))
            for i in project.tag:
                self.add_projectTag(str(project.ID), i)

            cursor.execute('delete from projectRelation where project1=%s', str(project.ID))
            for i in project.relatedProject:
                self.add_projectRelation(str(project.ID), i)

            cursor.execute('delete from projectDocument where projectID²=%s', str(project.ID))
            for i in project.desc:
                self.add_projectDocument(str(project.ID), i)
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change project')


class StudentAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect
        self.project = ProjectAccess(self.dbconnect)

    # returns all the bookmarks of the student
    def get_studentBookmarks(self, studentId):
        from Bookmark import Bookmark
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
            projects.append(self.project.get_project(row[0]))
        return projects

    # returns all bookmarks to a certain project
    def get_projectBookmarks(self, projectId):
        from Bookmark import Bookmark
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s', (str(projectId)))
        bookmarks = list()
        for row in cursor:
            bookmark = Bookmark(row[0], row[1])
            bookmarks.append(bookmark)
        return bookmarks

    def add_bookmark(self, projectId, studentId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s and student=%s', (str(projectId), str(studentId)))
        if cursor.rowcount == 0:
            cursor.execute('insert into bookmark values(%s,%s)', (str(projectId), str(studentId)))

    def get_students(self):
        from Student import Student
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from student')
        students = list()
        for row in cursor:
            student = Student(row[0], row[1])
            student.likedProject = self.get_studentBookmarkProject(student.studentID)
            students.append(student)
        return students

    def get_student(self, ID):
        from Student import Student
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM student WHERE studentID=%s ', (str(ID)))
        row = cursor.fetchone()
        stu = Student(row[0], row[1])
        stu.likedProject = self.get_studentBookmarkProject(stu.studentID)
        return stu

    def add_student(self, stu):
        cursor = self.dbconnect.get_cursor()
        try:
            if stu.studentId is not None:
                cursor.execute('INSERT INTO student values(%s,%s)',
                               (str(stu.studentId), stu.name))
            else:
                cursor.execute('INSERT INTO student values(default,%s)',
                               (stu.name))
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
        from ProjectRegistration import ProjectRegistration
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration')
        prs = list()
        for row in cursor:
            pr = ProjectRegistration(row[0], row[1], row[2])
            prs.append(pr)
        return prs

    def get_projectRegistrationsOnProject(self, projectID):
        from ProjectRegistration import ProjectRegistration
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration where project=%s', (str(projectID)))
        prs = list()
        for row in cursor:
            pr = ProjectRegistration(row[0], row[1], row[2])
            prs.append(pr)
        return prs

    def get_projectRegistrationsOnStudent(self, studentID):
        from ProjectRegistration import ProjectRegistration
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration where student=%s', (str(studentID)))
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

    def change_student(self, student):
        cursor = self.dbconnect.get_cursor()
        try:
            if student.studentID is None:
                raise Exception('no id given')
            cursor.execute('select * from student where studentID=%s', (str(student.studentID)))
            if cursor.rowcount == 0:
                raise Exception('no student found with that id')
            cursor.execute('update  student set name= %s where studentId=%s', (student.name, str(student.studentID)))

            cursor.execute('delete from bookmark where student=%s', str(student.studentID))
            for i in student.likedProject:
                self.add_bookmark(i, str(student.studentID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change student')


class DomainAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def add_discipline(self, discipline):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("INSERT INTO discipline (subject) VALUES (%s)", (discipline,))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to add discipline!\n(%s)' % (error))

    def remove_discipline(self, discipline):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("DELETE FROM discipline WHERE subject = (%s)", (discipline,))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to remove discipline!:\n(%s)' % (error))

    def get_disciplines(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from discipline')
        disciplines = list()
        for row in cursor:
            disciplines.append(row[0])
        return disciplines

    def add_title(self, title):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO title values(%s)', (title))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add title!')

    def get_titles(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from title')
        titles = list()
        for row in cursor:
            titles.append(row[0])
        return titles

    def add_intextOrigin(self, origin):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO INTEXT values(%s)', (origin))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add intext origin!')

    def get_intextOrigin(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from INTEXT')
        origins = list()
        for row in cursor:
            origins.append(row[0])
        return origins

    def add_registrationStatus(self, status):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO registration values(%s)', (status))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add registration status!')

    def get_registrationStatus(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from registration')
        status = list()
        for row in cursor:
            status.append(row[0])
        return status

    def add_language(self, lang):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO language values(%s)', (lang))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add language!')

    def get_languages(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from language')
        langs = list()
        for row in cursor:
            langs.append(row[0])
        return langs

    def add_projectType(self, type):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO projectType values(%s)', (type))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add projectType!')

    def get_projectType(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectType ')
        types = list()
        for i in cursor:
            types.append(i[0])
        return types


class FullDataAccess(DocumentAccess, DomainAccess, EmployeeAccess, ProjectAccess, StudentAccess, ResearchGroupAccess):
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect
        DomainAccess.__init__(self, self.dbconnect)
        DocumentAccess.__init__(self, self.dbconnect)
        EmployeeAccess.__init__(self, self.dbconnect)
        ProjectAccess.__init__(self, self.dbconnect)
        StudentAccess.__init__(self, self.dbconnect)
        ResearchGroupAccess.__init__(self, self.dbconnect)
