import dbConnection


class DocumentAccess:
    def __init__(self):
        """
        basic initialiser for a documentAcces
        :param dbconnect:
        """
        self.dbconnect = dbConnection.connection

    def get_documents(self):
        """
        gets all documents from the connected database
        :return: a list of documents
        """
        from Document import Document
        from Attachment import Attachment
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document')
        documents = list()
        for row in cursor:
            document = Document(row[0], row[1], row[2])
            cursorAttachment = self.dbconnect.get_cursor()
            cursorAttachment.execute('select * from attachment where %s=doc', (document.ID,))
            for att in cursorAttachment:
                document.attachment.append(Attachment(att[0], att[1]))
            documents.append(document)
        return documents

    def get_document(self, id):
        """
        gets a single document on a given id
        :param id: an id (will be casted to string)
        :return: a single doucment
        """
        from Document import Document
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM document WHERE documentID=%s', (id,))
        row = cursor.fetchone()
        document = Document(row[0], row[1], row[2])
        cursorAttachment = self.dbconnect.get_cursor()
        cursorAttachment.execute('select * from attachment where doc=%s', (document.ID,))
        for att in cursorAttachment:
            document.attachment.append(att[1])
        return document

    def add_attachment(self, documentID, attachment):
        """
        adds a new attachment to the database an couples it with a document
        :param documentID: the doucment id (will be casted to a string)
        :param attachment: the attachment
        """
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('select * from attachment where doc=%s and attachment=%s',
                           (documentID, attachment))
            if cursor.rowcount == 0:
                cursor.execute('insert into attachment values(%s,%s)', (documentID, str(attachment)))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save attachment!')

    # returns the document id of the added document
    def add_document(self, doc):
        """
        adds a document to the database and sets the id of the given document to the new one in the database
        :param doc: the document you are about to add (should not have an id)
        """
        cursor = self.dbconnect.get_cursor()
        try:
            id = None
            if doc.ID is None:
                cursor.execute('INSERT INTO document VALUES(default ,%s,%s)', (doc.language, str(doc.text)))
                cursor.execute('SELECT LASTVAL()')
                id = cursor.fetchone()[0]
                doc.ID = id
                for att in doc.attachment:
                    self.add_attachment(id, att)
            # get id and return updated object
            self.dbconnect.commit()
            return id
        except (Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('Unable to save document!%s' % error)

    def change_Document(self, document):
        """
        changes the doucment that is currcently already in the database
        :param document: a document with an id that is already in the database
        """
        try:
            if document.ID is not None:
                cursor = self.dbconnect.get_cursor()
                cursor.execute('select * from document where documentID=%s', (document.ID,))
                if cursor.rowcount == 0:
                    raise Exception('no document with that ID found')
                cursor.execute('update document set lang= %s, content= %s where documentID=%s',
                               (document.language, document.text, document.ID))

                cursor.execute('delete from attachment where doc=%s', (document.ID,))
                for i in document.attachment:
                    self.add_attachment(document.ID, i)
                self.dbconnect.commit()

            else:
                raise Exception('Document doesnt have ID')
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to change document!')


class ResearchGroupAccess:
    def __init__(self):
        """
        creates a researchGroup object
        """
        self.dbconnect = dbConnection.connection
        self.doc = DocumentAccess()

    def get_researchgroupDescriptions(self, groupid):
        """
        gets all descriptions of a researchgroup out of the database
        :param groupid: the id of the researchgroup
        :return: a list of descriptions
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from groupDescription where groupID=%s', (groupid,))
        desc = list()
        for row in cursor:
            desc.append(self.doc.get_document(row[1]))
        return desc

    def add_researchGroupDescription(self, document, groupid):
        """
        adds a new researchgroupDescription to the database
        :param document: the description you are adding
        :param groupid: the id of the researchgroup you are adding it to
        """
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.doc.add_document(document)
            cursor.execute('INSERT INTO groupDescription values(%s,%s)',
                           (groupid, docid))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save researchgroupdescription!')

    def get_researchGroups(self):
        """
        gets all researchgroups out of the database
        :return: a list of researchgroups
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from researchGroup')
        rgroups = list()
        for row in cursor:
            rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
            rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
            newcursor = self.dbconnect.get_cursor()
            newcursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
            if newcursor.rowcount > 0:
                rgroup.contactID = newcursor.fetchone()[0]
            rgroups.append(rgroup)
        return rgroups

    def get_researchGroupOnName(self, name):
        """
        gets a researchgroups based of a name
        :param name: the name of said researchgroup
        :return: a researchgroup object
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGroup WHERE name=%s', (name,))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
        if cursor.rowcount > 0:
            rgroup.contactID = cursor.fetchone()[0]
        return rgroup

    def get_researchGroupsOnIDs(self, ids):
        """
        gets a researchgroup from teh database based on an id
        :param id: the id
        :return: a researchgroup object
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()

        rgroups = list()

        for id in ids:
            cursor.execute('SELECT * FROM researchGroup WHERE groupID=%s', (id,))
            row = cursor.fetchone()
            rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
            rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
            cursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
            if cursor.rowcount > 0:
                rgroup.contactID = cursor.fetchone()[0]
            rgroups.append(rgroup)

        return rgroups

    def get_singleResearchGroupOnID(self, id):
        """

        :param id:
        :return:
        """
        from ResearchGroup import ResearchGroup
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM researchGroup WHERE groupID=%s', (id,))
        row = cursor.fetchone()
        rgroup = ResearchGroup(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None)
        rgroup.desc = self.get_researchgroupDescriptions(rgroup.ID)
        cursor.execute('select * from contactPerson where rgroup=%s', (rgroup.ID,))
        if cursor.rowcount > 0:
            rgroup.contactID = cursor.fetchone()[0]
        return rgroup

    def remove_researchGroup(self, id):
        """
        removes a researchgroup from the database based on an id
        :param id: the id
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM researchGroup WHERE groupID=%s', (id,))
        self.dbconnect.commit()

    def changeContactPerson(self, eid, groupID):
        """
        changes a contact person for a researchgroup
        :param eid: the new employee that will become the contactperson
        :param groupID: the researchgroup id
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('SELECT * FROM contactPerson WHERE rgroup=%s', (groupID,))
            if cursor.rowcount == 0:
                cursor.execute('insert into contactperson values(%s,%s)', (eid, groupID))
            else:
                if (cursor.fetchone()[0] != eid):
                    # waarom zegt pycharm hier constant dat hem '=' verwacht terwijl dat er staat ???
                    cursor.execute('update contactPerson set employee= %s where rgroup=%s', (eid, groupID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to check contactperson !')

    def add_researchGroup(self, group):
        """
        adds a new researchgroup to the database
        :param group: the new resrachgroup (without an id)
        """
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
        """
        changes a researchgroup in the database
        :param group: the researchgroup that it will be changed into
        """
        cursor = self.dbconnect.get_cursor()
        try:
            if group.ID is None:
                raise Exception('no id given')
            cursor.execute('select * from researchgroup where groupID=%s', (group.ID,))
            if cursor.rowcount == 0:
                raise Exception('no researchGroup found with that id')
            cursor.execute(
                'update researchGroup set name= %s,abbreviation= %s,discipline= %s,active= %s,address= %s,telNr= %s where groupId=%s',
                (group.name, group.abbreviation, group.discipline, group.active, group.address, str(group.telNr)),
                str(group.ID))
            cursor.execute('delete from groupDescription where groupID=%s', (group.ID,))
            for i in group.desc:
                self.add_researchGroupDescription(i, str(group.ID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change researchGroup')


class EmployeeAccess:
    def __init__(self):
        """
        a constructor for an EmployeeAccess object
        """
        self.dbconnect = dbConnection.connection

    def get_employees(self):
        """
        get all the employees out of the database
        :return: a list of employees
        """
        from Employee import Employee
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employee')

        employees = list()
        for row in cursor:
            employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            employees.append(employee)
        return employees

    def get_employee(self, id):
        """
        gets a single employee out the database on an id
        :param id: the id
        :return: a single employee
        """
        from Employee import Employee
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE employeeID=%s ', (id,))
        row = cursor.fetchone()
        return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

    def get_employeeOnName(self,name):
        """
        gets a single employee out the database on a name
        :param name: the name
        :return: a single employee
        """
        from Employee import Employee
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE name=%s ', (name,))
        if(cursor.rowcount!=0):
            row = cursor.fetchone()
            return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        else:
            return None

    def add_employee(self, empl):
        """
        adds an employee to the database
        :param empl: the new employee (without id)
        :return:
        """
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
        """
        removes an emplouee out the database
        :param id: the id of the employee you are removing
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM employee WHERE employeeID=%s', (id,))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to remove Employee!\n(%s)' % (error))

    def filter_employees(self, searchQuery="", researchGroup="", promotor=0, ):
        """
        does a filter on all the employees in the database
        :param searchQuery: search on a name
        :param researchGroup: search on a researchgroup
        :param promotor: search for promoters
        :return: a list of employee that passess the needed filters
        """
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
        """
        adds a role to an employee
        :param id: the id of the employee
        :param role: the role that will be added
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO employeeRoles values(%s,%s)',
                           (id, role))
            # get id and return updated object
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to save EmployeeRole!\n(%s)' % (error))

    def get_employeeRoles(self, id):
        """
        gets al the roles of an employee
        :param id: the id of the employee
        :return: a list of roles that the employee has
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from employeeRoles where employee=%s', (id,))
        roles = list()
        for row in cursor:
            roles.append(row[1])
        return roles

    def change_employee(self, employee):
        """
        changes the data of an employee
        :param employee: the new data fro employee
        """
        cursor = self.dbconnect.get_cursor()
        try:
            if employee.ID == None:
                raise Exception('no id given')
            cursor.execute('select * from employee where employeeID=%s', (employee.ID,))
            if cursor.rowcount == 0:
                raise Exception('no employee found with that id')
            cursor.execute(
                'update employee set name= %s,email= %s,office= %s,researchgroup= %s,title= %s,INTernORextern= %s,active= %s,promotor= %s where employeeID=%s',
                (employee.name, employee.email, employee.office, employee.research_group, employee.title,
                 employee.internOrExtern, employee.active, employee.promotor, employee.ID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change employee')

    def get_employeeProjects(self, id):
        """
        get all the projects of an employee IMPORTANT  not all fields will be completed only the fields in the project table and that of the activeYears
        :param id: the id of the employee
        :return: a list of all the projects where the employee is a promotor
        """
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select project from projectpromotor where employee=%s', (id,))

        projectsId = list()
        for row in cursor:
            projectsId.append(row[0])

        projects = list()
        for projId in projectsId:
            cursor.execute('select * from project where projectID=%s',
                           (projId,))  # returns exactly one row from the table
            row = cursor.fetchone()
            project = Project(row[0], row[1], row[2], row[3])

            cursor.execute('select year from projectYearConnection where projectID=%s', (projId,))

            years = list()
            for row in cursor:
                years.append(row[0])

            project.activeYear = years

            projects.append(project)

        return projects


class ProjectAccess:
    def __init__(self):
        """
        a constructor for a projectAccess class
        """
        self.dbconnect = dbConnection.connection
        self.doc = DocumentAccess()

    def get_projectDocuments(self, projectID):
        """
        get all the documents for a certain project
        :param projectID: the id of the project
        :return: a list of documents
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectDocument where projectID=%s', (projectID,))
        desc = list()
        for row in cursor:
            desc.append(self.doc.get_document(row[1]))

        return desc

    def add_projectDocument(self, projectID, document):
        """
        adds a document to a project
        :param projectID: the id of the project
        :param document: the full document
        """
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.doc.add_document(document)
            cursor.execute('INSERT INTO projectDocument values(%s,%s)',
                           (projectID, docid))

            # get id and return updated object
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectdocument!\n%s' % error)

    def get_projectYears(self, projectID):
        """
        gets all the years a project is active
        :param projectID: the id of the project
        :return: a list of years
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectYearConnection where projectID=%s', (projectID,))
        years = list()
        for i in cursor:
            years.append(i[0])
        return years

    def add_projectYears(self, projectId, year):
        """
        adds a year to a project
        :param projectId: the id of the project
        :param year: the year you are adding
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectYear where year=%s', (year,))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectYear values(%s)', (year,))
            cursor.execute('select * from projectYearConnection where year=%s and projectID=%s',
                           (year, projectId))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectYearConnection values(%s,%s)', (year, projectId))
            self.dbconnect.commit()
        except (Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectYear!\n%s' % error)

    def get_typesFromProject(self, projectID):
        """
        get all the types of a certain project
        :param projectID: the id of a the project
        :return: a list of types
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectYearConnection where projectID=%s', (projectID,))
        types = list()
        for i in cursor:
            types.append(i[0])
        return types

    def add_projectTypeConnection(self, projectId, type):
        """
        adds a new type to a project
        :param projectId: the id of the project
        :param type: the type you want to add
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectTypeConnection where type=%s and projectID=%s',
                           (str(type), projectId))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectTypeConnection values(%s,%s)', (str(type), projectId))
                self.dbconnect.commit()
        except (Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectType!\n%s' % error)

    def get_projectPromotors(self, projectID):
        """
        gets all the promotors for a certain project
        :param projectID: the id of the project
        :return: a list of ids for the promoters
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectPromotor where project=%s', (projectID,))
        proms = list()
        for row in cursor:
            proms.append(row[0])
        return proms

    def add_projectPromotor(self, projectID, employeeId):
        """
        adds a promotor to a certain project in the database
        :param projectID: the id of the project
        :param employeeId: the id of the employee
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectPromotor where employee=%s and project=%s',
                           (employeeId, projectID))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectPromotor values(%s,%s)', (employeeId, projectID))
                self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            print("unable to safe promotor\n%s" % error)

    def get_projectTags(self, projectID):
        """
        gets all tags for a project
        :param projectID: the id of said project
        :return: a list of tags
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectTag where project=%s', (projectID,))
        tags = list()
        for row in cursor:
            tags.append(row[0])
        return tags

    def delete_all_ProjectTages(self):
        """
        deletes all tags in the database, this is used for when the new tags are calculated
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM projecttag')
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            print("unable to delete all tags")

    def add_projectTag(self, projectID, tag):
        """
        adds a tag to a project
        :param projectID: the id of the project
        :param tag: the tag you want to add
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectTag where tag=%s and project=%s', (str(tag), str(projectID)))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectTag values(%s,%s)', (str(tag), projectID))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            print("unable to save tag")

    def get_projectRelations(self, projectID):
        """
        get all related projects for a certain project
        :param projectID: the id you want the related projectss for
        :return:a list of related projects id's
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRelation where project1=%s', (projectID,))
        related = list()
        for row in cursor:
            related.append(row[1])
        cursor.execute('select * from projectRelation where project2=%s', (projectID,))
        for row in cursor:
            if row[0] not in related:
                related.append(row[0])
        return related

    def add_projectRelation(self, project1ID, project2ID):
        """
        adds a relation between 2 projects
        :param project1ID: the id of the first project
        :param project2ID: the id of the second project
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from  projectRelation where project1=%s and project2=%s',
                           (project1ID, project2ID))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectRelation values(%s,%s)', (project1ID, project2ID))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            print("unable to save tag")

    def get_projectresearchgroups(self, projectID):
        """
        gets all the researchgroup id's of a project on a certain id
        :param projectID: the id of the project
        :return: a list of researchgroups
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectResearchgroup where projectid=%s', (projectID,))
        projects = list()
        for row in cursor:
            projects.append(row[1])
        return projects

    def add_projectResearchgroup(self, projectID, researchgroupID):
        """
        adds a relation between a project and a resaerchgroup
        :param projectid: the project
        :param researchgroupID: the researchgroup
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from  projectResearchgroup where projectid=%s and researchgroupid=%s',
                           (projectID, researchgroupID))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectResearchgroup values(%s,%s)', (projectID, researchgroupID))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            print("unable to save projectresearchgroup")

    def get_projects_of_employee(self, employeeID):
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from project JOIN projectpromotor p on project.projectid = p.project WHERE p.employee=%s', str(employeeID))
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3])
            projects.append(project)
        return projects

    def get_projects(self):
        """
        gets all project
        :return: a list of projects
        """
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        sql = "select * from project;"
        cursor.execute(sql)
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3])
            projects.append(project)

        # de ,'s zijn nodig om de types over te laten gaan in tuples, anders zal dit fouten geven.
        for project in projects:
            cursor.execute('SELECT type FROM projectTypeConnection WHERE projectID=%s', (project.ID,))
            project.type = list(cursor.fetchall())

            project.desc = self.get_projectDocuments(project.ID)

            cursor.execute('SELECT discipline FROM projectDiscipline WHERE projectID=%s', (project.ID,))
            project.discipline = list(cursor.fetchall())

            cursor.execute('SELECT student FROM projectRegistration WHERE project=%s AND status=%s',
                           (project.ID, "succeeded"))
            project.registeredStudents = list(cursor.fetchall())

            project.researchGroup = self.get_projectresearchgroups(project.ID)

            cursor.execute('SELECT project2 FROM projectRelation WHERE project1=%s', (project.ID,))
            project.relatedProject = list(cursor.fetchall())

            cursor.execute('SELECT employee FROM projectPromotor WHERE project=%s', (project.ID,))
            project.promotor = list(cursor.fetchall())

            cursor.execute('SELECT tag FROM projectTag WHERE project=%s', (project.ID,))
            project.tag = list(cursor.fetchall())

            cursor.execute('SELECT year FROM projectYearConnection WHERE projectID=%s', (project.ID,))
            project.activeYear = list(cursor.fetchall())

        return projects

    def get_project(self, ID):
        """
        gets a single project on an id
        :param ID: the id
        :return: a single project
        """
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM project WHERE projectID=%s ', (ID,))
        row = cursor.fetchone()
        project = Project(row[0], row[1], row[2], row[3])
        project.desc = self.get_projectDocuments(project.ID)
        project.activeYear = self.get_projectYears(project.ID)
        project.promotor = self.get_projectPromotors(project.ID)
        project.tag = self.get_projectTags(project.ID)
        project.relatedProject = self.get_projectRelations(project.ID)
        project.researchGroup = self.get_projectresearchgroups(project.ID)
        return project

    def remove_project(self, ID):
        """
        removes a project from the database
        :param ID: the id of the project you want to remove
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('DELETE FROM project WHERE projectID=%s', (ID,))
        self.dbconnect.commit()
        return

    def get_project_filter_data(self):
        from Project import Project
        cursor = self.dbconnect.get_cursor()
        # sql = "SELECT p.projectid, title, maxstudents, p.active, name, discipline, type FROM (project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup)" \
        #       "INNER JOIN projectTypeConnection ON p.projectid=projectTypeConnection.projectID"

        # TODO: dit werkt niemeer :(
        # sql = "SELECT p.projectid, title, maxstudents, p.active, name, discipline, type, (" \
        #       "SELECT COUNT(*) FROM projectregistration pr WHERE pr.project=p.projectid) as cnt " \
        #       "FROM (project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup)" \
        #       "INNER JOIN projectTypeConnection ON p.projectid=projectTypeConnection.projectID"

        # temp query
        sql = "select * from project;"
        cursor.execute(sql)
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3])
            projects.append(project)

        # de ,'s zijn nodig om de types over te laten gaan in tuples, anders zal dit fouten geven.
        for project in projects:
            cursor.execute('SELECT type FROM projectTypeConnection WHERE projectID=%s', (project.ID,))
            project.type = list(cursor.fetchall())

            project.desc = self.get_projectDocuments(project.ID)

            cursor.execute('SELECT discipline FROM projectDiscipline WHERE projectID=%s', (project.ID,))
            project.discipline = list(cursor.fetchall())

            cursor.execute('SELECT student FROM projectRegistration WHERE project=%s AND status=%s',
                           (project.ID, "succeeded"))
            project.registeredStudents = len(list(cursor.fetchall()))

            cursor.execute('SELECT researchgroupid FROM projectResearchgroup WHERE projectID=%s', (project.ID,))
            project.researchGroup = list(cursor.fetchall())

            cursor.execute('SELECT project2 FROM projectRelation WHERE project1=%s', (project.ID,))
            project.relatedProject = list(cursor.fetchall())

            cursor.execute('SELECT employee FROM projectPromotor WHERE project=%s', (project.ID,))
            project.promotor = list(cursor.fetchall())

            cursor.execute('SELECT tag FROM projectTag WHERE project=%s', (project.ID,))
            project.tag = list(cursor.fetchall())

            cursor.execute('SELECT year FROM projectYearConnection WHERE projectID=%s', (project.ID,))
            project.activeYear = list(cursor.fetchall())

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
        """
        adds a project to the database
        :param proj: the project that will be added (should not have an id)
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO project values(default,%s,%s,%s)',
                           (proj.title, str(proj.maxStudents), proj.active))
            cursor.execute('SELECT LASTVAL()')
            gid = cursor.fetchone()
            proj.ID = int(gid[0])
            for i in proj.desc:
                self.add_projectDocument(proj.ID, i)
            for i in proj.activeYear:
                self.add_projectYears(proj.ID, i)
            for i in proj.type:
                self.add_projectTypeConnection(proj.ID, i)
            for i in proj.tag:
                self.add_projectTag(proj.ID, i)
            for i in proj.relatedProject:
                self.add_projectRelation(proj.ID, i)
            for i in proj.promotor:
                self.add_projectPromotor(proj.ID, i)
            for i in proj.researchGroup:
                self.add_projectResearchgroup(proj.ID, i)
            self.dbconnect.commit()
        except (Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('Unable to save project!\n%s' % error)

    def change_project(self, project):
        """
        change the data of a project that already is in the database
        :param project: the project that will be changed
        """
        cursor = self.dbconnect.get_cursor()
        try:
            if project.ID == None:
                raise Exception('no id given')
            cursor.execute('select * from project where projectID=%s', (project.ID,))
            if cursor.rowcount == 0:
                raise Exception('no project found with that id')
            cursor.execute(
                'update project set title= %s,maxStudents= %s,active= %s,researchGroup= %s where projectID=%s',
                (project.title, project.maxStudents, project.active, project.researchGroup, project.ID))

            cursor.execute('delete from projectYearConnection where projectID=%s', (project.ID,))
            for i in project.activeYear:
                self.add_projectYears(project.ID, i)

            cursor.execute('delete from projectTypeConnection where projectID=%s', (project.ID,))
            for i in project.type:
                self.add_projectTypeConnection(project.ID, i)

            cursor.execute('delete from projectPromotor where project=%s', (project.ID,))
            for i in project.promotor:
                self.add_projectPromotor(project.ID, i)

            cursor.execute('delete from projectTag where project=%s', (project.ID,))
            for i in project.tag:
                self.add_projectTag(project.ID, i)

            cursor.execute('delete from projectRelation where project1=%s', (project.ID,))
            for i in project.relatedProject:
                self.add_projectRelation(project.ID, i)

            cursor.execute('delete from projectDocument where projectID=%s', (project.ID,))
            for i in project.desc:
                self.add_projectDocument(project.ID, i)

            cursor.execute('delete from projectresearchgroup where projectid=%s', (project.ID,))
            for i in project.researchGroup:
                self.add_projectDocument(project.ID, i)
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change project')


class StudentAccess:
    def __init__(self):
        """
        a constructor for a studentAccess object
        """
        self.dbconnect = dbConnection.connection
        self.project = ProjectAccess()

    # returns all the bookmarks of the student
    def get_studentBookmarks(self, studentId):
        """
        gets all the bookmarks that a student has
        :param studentId: the id of said student
        :return: a list of bookmarks (project id's and student id's)
        """
        from Bookmark import Bookmark
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where student=%s', (studentId,))
        bookmarks = list()
        for row in cursor:
            bookmarker = Bookmark(row[0], row[1])
            bookmarks.append(bookmarker)
        return bookmarks

    # return the projects of all the bookmarks a student has
    def get_studentBookmarkProject(self, studentId):
        """
        gets all the bookmarks a student has in project forl
        :param studentId: the student id
        :return: a list of projects
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where student=%s', (studentId,))
        projects = list()
        for row in cursor:
            projects.append(self.project.get_project(row[0]))
        return projects

    # returns all bookmarks to a certain project
    def get_projectBookmarks(self, projectId):
        """
        get all the bookmars that a certai  project has
        :param projectId: the id of said project
        :return: a list of bookmars (student and project id's)
        """
        from Bookmark import Bookmark
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s', (projectId,))
        bookmarks = list()
        for row in cursor:
            bookmark = Bookmark(row[0], row[1])
            bookmarks.append(bookmark)
        return bookmarks

    def add_bookmark(self, projectId, studentId):
        """
        adds a new bookmars
        :param projectId: the project id
        :param studentId: the student id
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from bookmark where project=%s and student=%s', (projectId, studentId))
        if cursor.rowcount == 0:
            cursor.execute('insert into bookmark values(%s,%s)', (projectId, studentId))

    def get_students(self):
        """
        gets all students out of the database
        :return: a list of students
        """
        from Student import Student
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from student')
        students = list()
        for row in cursor:
            student = Student(row[0], row[1], row[2])
            student.likedProject = self.get_studentBookmarkProject(student.studentID)
            students.append(student)
        return students

    def get_student(self, ID):
        """
        gets a single student based of an id
        :param ID: the id of this student
        :return: a single student
        """
        from Student import Student
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM student WHERE studentID=%s ', (ID,))
        row = cursor.fetchone()
        stu = Student(row[0], row[1], row[2])
        stu.likedProject = self.get_studentBookmarkProject(stu.studentID)
        return stu

    def get_studentOnStudentNumber(self,number):
        """
        gets a single student based of an id
        :param ID: the id of this student
        :return: a single student
        """
        from Student import Student
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM student WHERE studentnumber=%s ', (number,))
        if(cursor.rowcount!=0):
            row = cursor.fetchone()
            stu = Student(row[0], row[1], row[2])
            stu.likedProject = self.get_studentBookmarkProject(stu.studentID)
            return stu
        else:
            return None

    def add_student(self, stu):
        """
        adds a student to the database
        :param stu: a new student(should be without id)
        """
        cursor = self.dbconnect.get_cursor()
        try:
            if stu.studentId is not None:
                cursor.execute('INSERT INTO student values(%s,%s,%s)',
                               (stu.studentId, stu.name, stu.studentNumber))
            else:
                cursor.execute('INSERT INTO student values(default,%s,%s)',
                               (stu.name, stu.studentNumber))
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
        """
        get all projectregistrations
        :return: a list of projectregistration
        """
        from ProjectRegistration import ProjectRegistration
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration')
        prs = list()
        for row in cursor:
            pr = ProjectRegistration(row[0], row[1], row[2])
            prs.append(pr)
        return prs

    def get_projectRegistrationsOnProject(self, projectID):
        """
        gets all projectregistrations for a certain project
        :param projectID: the id of the project
        :return: a list of projectregistrations
        """
        from ProjectRegistration import ProjectRegistration
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration where project=%s', (projectID,))
        prs = list()
        for row in cursor:
            pr = ProjectRegistration(row[0], row[1], row[2])
            prs.append(pr)
        return prs

    def get_projectRegistrationsOnStudent(self, studentID):
        """
        gets all projectregistrations for a certain student
        :param studentID: the id of the student
        :return: a list of projectregistrations
        """
        from ProjectRegistration import ProjectRegistration
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectRegistration where student=%s', (studentID,))
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

    def add_projectRegistration(self, pr, student):
        """
        adds a new projecctregistration
        :param pr: the project
        :param student: the studentId
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO projectRegistration values(%s,%s,%s)',
                           (pr.project, str(pr.status), student))
            # get id and return updated object
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to save project registration!')

    def change_student(self, student):
        """
        changes a student that already is in the database
        :param student: the student that will be changed
        """
        cursor = self.dbconnect.get_cursor()
        try:
            if student.studentID is None:
                raise Exception('no id given')
            cursor.execute('select * from student where studentID=%s', (student.studentID,))
            if cursor.rowcount == 0:
                raise Exception('no student found with that id')
            cursor.execute('update  student set name= %s, set studentnumber=%s where studentId=%s',
                           (student.name, student.studentNumber, student.studentID))

            cursor.execute('delete from bookmark where student=%s', (student.studentID,))
            for i in student.likedProject:
                self.add_bookmark(i, str(student.studentID))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change student')


class DomainAccess:
    def __init__(self):
        """
        constructor for a domainAccess object
        """
        self.dbconnect = dbConnection.connection

    def add_discipline(self, discipline):
        """
        adds a discipline to the list of disciplines
        :param discipline: the new discipline
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("INSERT INTO discipline (subject) VALUES (%s)", (discipline,))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to add discipline!\n(%s)' % (error))

    def remove_discipline(self, discipline):
        """
        removes a discipline
        :param discipline:
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("DELETE FROM discipline WHERE subject = (%s)", (discipline,))
            self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('\nUnable to remove discipline!:\n(%s)' % (error))

    def get_disciplines(self):
        """
        gets all disciplines
        :return: a list of disciplines
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from discipline')
        disciplines = list()
        for row in cursor:
            disciplines.append(row[0])
        return disciplines

    def add_title(self, title):
        """
        adds a title to the list of titles
        :param title:
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO title values(%s)', (title,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add title!')

    def get_titles(self):
        """
        gets all titles out of the database
        :return: a list of titles
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from title')
        titles = list()
        for row in cursor:
            titles.append(row[0])
        return titles

    def add_intextOrigin(self, origin):
        """
        adds a new intextOrigin to the database
        :param origin: the new thing
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO INTEXT values(%s)', (origin,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add intext origin!')

    def get_intextOrigin(self):
        """
        gets all intextorigins out of the database
        :return: a list of origins (intern, extern, etc
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from INTEXT')
        origins = list()
        for row in cursor:
            origins.append(row[0])
        return origins

    def add_registrationStatus(self, status):
        """
        adds a new refistration status to the list
        :param status: the new status
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO registration values(%s)', (status,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add registration status!')

    def get_registrationStatus(self):
        """
        gets all registrationStatusses
        :return: a list of statusses
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from registration')
        status = list()
        for row in cursor:
            status.append(row[0])
        return status

    def add_language(self, lang):
        """
        adds a new language to the list of languages
        :param lang: the new language
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO language values(%s)', (lang,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add language!')

    def get_languages(self):
        """
        gets all languages out of the database
        :return: a list of languages
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from language')
        langs = list()
        for row in cursor:
            langs.append(row[0])
        return langs

    def add_projectType(self, type):
        """
        adds a new projectType to the database
        :param type: the new type
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO projectType values(%s)', (type,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('Unable to add projectType!')

    def get_projectType(self):
        """
        gets all projectTyppes out of the database
        :return: a list of projecTypes
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectType ')
        types = list()
        for i in cursor:
            types.append(i[0])
        return types


class FullDataAccess(DocumentAccess, DomainAccess, EmployeeAccess, ProjectAccess, StudentAccess, ResearchGroupAccess):
    def __init__(self):
        """
        this constructor makes a FullDataAccess object that has access to all the access classes
        """

        DomainAccess.__init__(self)
        DocumentAccess.__init__(self)
        EmployeeAccess.__init__(self)
        ProjectAccess.__init__(self)
        StudentAccess.__init__(self)
        ResearchGroupAccess.__init__(self)
