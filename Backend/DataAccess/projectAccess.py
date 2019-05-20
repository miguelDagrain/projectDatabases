import dbConnection

from DataAccess.documentAccess import DocumentAccess


class ProjectAccess:
    def __init__(self):
        """
        a constructor for a projectAccess class
        """
        self.dbconnect = dbConnection.connection
        self.doc = DocumentAccess()

    def add_externEmployee(self,projectID,name):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("execute insertExternEmployee(%s,%s)",(str(projectID),name,))
            self.dbconnect.commit()
        except Exception as e:
            self.dbconnect.rollback()
            print("unable to add external employee"+str(e))

    def delete_projectExternEmployees(self,projectID):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("execute deleteProjectExternEmployees (%s)", (str(projectID),))
            self.dbconnect.commit()
        except Exception as e:
            self.dbconnect.rollback()
            print("unable to delete external employees from a project" + str(e))

    def get_externalEmployeesFromProject(self,projectID):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute("execute getProjectExternEmployees (%s)", (str(projectID),))
            employees=list()
            for row in cursor:
                employees.append(row[1])
            return employees
        except Exception as e:
            self.dbconnect.rollback()
            print("unable to get external employees from a project" + str(e))

    def remove_bookmark(self, projectID, studentID):
        cursor = self.dbconnect.get_cursor()
        sql = 'DELETE FROM bookmark b WHERE b.project= %s AND b.student= %s'
        try:
            cursor.execute(sql, (str(projectID), str(studentID),))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception(
                "Unable to delete bookmark with projectID=" + str(projectID) + " and studentID=" + str(studentID))

    def change_title(self, projectID, newTitle):
        cursor = self.dbconnect.get_cursor()
        sql = 'UPDATE project SET title= %s WHERE projectID=%s'
        try:
            cursor.execute(sql, (str(newTitle), str(projectID)))
            self.dbconnect.commit()
            return True
        except:
            self.dbconnect.rollback()
        return False

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
        :param document: the full document with ID of -1
        """
        cursor = self.dbconnect.get_cursor()
        try:
            docid = self.doc.add_document(document)
            cursor.execute('INSERT INTO projectDocument values(%s,%s)',
                           (projectID, docid))

            # get id and return updated object
            document.ID = docid
            self.dbconnect.commit()
            return document
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
        cursor.execute('select * from projecttypeConnection where projectID=%s', (projectID,))
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

    def add_projectDiscipline(self, projectID, discipline):
        """
        adds a new discipline to a project
        :param projectID: the id of the project
        :param discipline: teh discipline you want to add
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectDiscipline where discipline=%s and projectID=%s',
                           (str(discipline), projectID))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectDiscipline values(%s, %s)', (projectID, str(discipline)))
                self.dbconnect.commit()
        except (Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            raise Exception('Unable to save projectDiscipline!\n%s' % error)

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

    def get_projectStaff(self, projectID):
        """
        gets all the staff not promotor for a certain project
        :param projectID: the id of the project
        :return: a list of ids for the promoters
        """
        cursor = self.dbconnect.get_cursor()
        cursor.execute('select * from projectStaff where project=%s', (projectID,))
        staff = list()
        for row in cursor:
            staff.append(row[0])
        return staff

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

    def add_projectStaff(self, projectID, employeeId):
        """
        adds a staff to a certain project in the database
        :param projectID: the id of the project
        :param employeeId: the id of the employee
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('select * from projectStaff where employee=%s and project=%s',
                           (employeeId, projectID))
            if cursor.rowcount == 0:
                cursor.execute('insert into projectStaff values(%s,%s)', (employeeId, projectID))
                self.dbconnect.commit()
        except(Exception, self.dbconnect.get_error()) as error:
            self.dbconnect.rollback()
            print("unable to safe staff\n%s" % error)

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
        except Exception as e:
            self.dbconnect.rollback()
            print("unable to save projectresearchgroup " + str(e))
            raise e

    def get_number_of_inactive_by_employee(self, employeeID):
        cursor = self.dbconnect.get_cursor()
        sql = \
            'SELECT count(distinct project.projectid) ' \
            'FROM project JOIN projectpromotor p ON project.projectid = p.project ' \
            'WHERE p.employee=%s AND project.active=false'
        cursor.execute(sql, (str(employeeID),))
        count = int(cursor.fetchone()[0])
        sql = \
            'SELECT count(distinct project.projectid) ' \
            'FROM project JOIN projectstaff p on project.projectid = p.project ' \
            'WHERE p.employee=%s AND project.active=false'
        cursor.execute(sql, (str(employeeID),))
        count += int(cursor.fetchone()[0])
        return count

    def get_projects_of_employee(self, employeeID):
        from Project import Project
        from DataAccess.studentAccess import StudentAccess
        cursor = self.dbconnect.get_cursor()
        # cursor.execute('select * from project JOIN projectpromotor p on project.projectid = p.project WHERE p.employee=%s', str(employeeID))
        cursor.execute(
            'select * from project JOIN projectpromotor p on project.projectid = p.project WHERE p.employee=%s',
            (str(employeeID),))
        projects = list()
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3])
            projects.append(project)

        cursor.execute(
            'select * from project JOIN projectstaff p on project.projectid = p.project WHERE p.employee=%s',
            (str(employeeID),))
        for row in cursor:
            project = Project(row[0], row[1], row[2], row[3])
            projects.append(project)

        for project in projects:
            cursor.execute('SELECT type FROM projectTypeConnection WHERE projectID=%s', (project.ID,))
            project.type = list(cursor.fetchall())
            project.desc = self.get_projectDocuments(project.ID)
            cursor.execute('SELECT discipline FROM projectDiscipline WHERE projectID=%s', (project.ID,))
            project.discipline = list(cursor.fetchall())
            cursor.execute('SELECT student FROM projectRegistration WHERE project=%s AND status=%s',
                           (project.ID, "succeeded"))
            reg_students = list(cursor.fetchall())
            project.registeredStudents = reg_students
            project.register_count = len(reg_students)
            project.researchGroup = self.get_projectresearchgroups(project.ID)
            cursor.execute('SELECT project2 FROM projectRelation WHERE project1=%s', (project.ID,))
            project.relatedProject = list(cursor.fetchall())
            cursor.execute('SELECT employee FROM projectPromotor WHERE project=%s', (project.ID,))
            project.promotors = list(cursor.fetchall())
            cursor.execute('SELECT tag FROM projectTag WHERE project=%s', (project.ID,))
            project.tag = list(cursor.fetchall())
            project.activeYear=self.get_projectYears(project.ID)
            project.extern_employees=self.get_externalEmployeesFromProject(project.ID)

            sa = StudentAccess()
            registrations = sa.get_projectRegistrationsOnProject(project.ID)
            project.registeredStudents = list()
            for i in registrations:
                project.registeredStudents.append(sa.get_student(i.student))

            descriptions = self.get_projectDocuments(project.ID)
            project.desc = descriptions
            for desc in descriptions:
                if desc.language == 'dutch':
                    project.desc_nl = desc
                elif desc.language == 'english':
                    project.desc_en = desc

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
            project.promotors = list(cursor.fetchall())

            cursor.execute('SELECT tag FROM projectTag WHERE project=%s', (project.ID,))
            project.tag = list(cursor.fetchall())

            project.extern_employees=self.get_externalEmployeesFromProject(project.ID)

            project.activeYear=self.get_projectYears(project.ID)

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
        if (cursor.rowcount == 0): return None
        row = cursor.fetchone()
        project = Project(row[0], row[1], row[2], row[3])
        project.desc = self.get_projectDocuments(project.ID)
        project.activeYear = self.get_projectYears(project.ID)
        project.promotors = self.get_projectPromotors(project.ID)
        project.tag = self.get_projectTags(project.ID)
        project.relatedProject = self.get_projectRelations(project.ID)
        project.researchGroup = self.get_projectresearchgroups(project.ID)
        project.type=self.get_typesFromProject(project.ID)
        project.extern_employees = self.get_externalEmployeesFromProject(project.ID)
        return project

    def remove_project(self, ID):
        """
        removes a project from the database
        :param ID: the id of the project you want to remove
        """
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('DELETE FROM project WHERE projectID=%s', (ID,))
            self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to remove project')

    def get_project_filter_data(self):
        from Project import Project
        try:
            cursor = self.dbconnect.get_cursor()
            # sql = "SELECT p.projectid, title, maxstudents, p.active, name, discipline, type FROM (project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup)" \
            #       "INNER JOIN projectTypeConnection ON p.projectid=projectTypeConnection.projectID"

            # TODO: dit werkt niemeer :(
            # sql = "SELECT p.projectid, title, maxstudents, p.active, name, discipline, type, (" \
            #       "SELECT COUNT(*) FROM projectregistration pr WHERE pr.project=p.projectid) as cnt " \
            #       "FROM (project p INNER JOIN researchGroup ON researchGroup.groupID=p.researchGroup)" \
            #       "INNER JOIN projectTypeConnection ON p.projectid=projectTypeConnection.projectID"

            # temp query
            sql = "select * from project Where active = TRUE;"
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
                project.promotors = list(cursor.fetchall())

                cursor.execute('SELECT tag FROM projectTag WHERE project=%s', (project.ID,))
                project.tag = list(cursor.fetchall())

                project.extern_employees = self.get_externalEmployeesFromProject(project.ID)

                project.activeYear=self.get_projectYears(project.ID)


            return projects
        except:
            self.dbconnect.rollback()
            raise Exception('unable to get project filter data')

    def get_promotors_and_associated_projects(self):
        """
        Get all promotors with their associated project Id's
        :return:
        """
        import sys

        cursor = self.dbconnect.get_cursor()
        employees = {}
        cursor.execute('SELECT employeeID, name FROM employee')


        for row in cursor:
            #print(row[0], file=sys.stdout)
            employees[row[0]] = {}
            employees[row[0]]['name'] = row[1]

        for id in employees.keys():
            #print(id, file=sys.stdout)
            projects = self.get_employee_projects_IDs(id)
            employees[id]['projects'] = projects

        return employees

    def get_employee_projects_IDs(self, ID):

        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT project FROM projectPromotor WHERE employee = %s', (ID,))
        projects = []
        for row in cursor:
            projects.append(row[0])

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
            for i in proj.promotors:
                self.add_projectPromotor(proj.ID, i)
            for i in proj.supervisors:
                self.add_projectStaff(proj.ID, i)
            for i in proj.researchGroup:
                self.add_projectResearchgroup(proj.ID, i)
            for i in proj.extern_employees:
                self.add_externEmployee(proj.ID,i)
            for i in proj.discipline:
                self.add_projectDiscipline(proj.ID,i)

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
            if project.ID is None:
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

            self.delete_projectExternEmployees(project.ID)
            for i in project.extern_employees:
                self.add_externEmployee(project.ID,i)
        except:
            self.dbconnect.rollback()
            raise Exception('unable to change project')
