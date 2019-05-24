import dbConnection

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

    def get_admins(self):
        """
        this function gets all the admins from the database
        :return: a list of employees that are also admins
        """
        from Employee import Employee
        admins = list()
        cursorRoles = self.dbconnect.get_cursor()
        cursorRoles.execute('select * from employeeRoles where role=\'admin\'')
        for row in cursorRoles:
            admins.append(self.get_employee(row[0]))
        return admins

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

    def get_employeeOnName(self, name):
        """
        gets a single employee out the database on a name
        :param name: the name
        :return: a single employee
        """
        from Employee import Employee
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM employee WHERE name=%s ', (name,))
        if (cursor.rowcount != 0):
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
                           (empl.name, empl.email, empl.office, empl.research_group, empl.title, empl.internOrExtern,
                            empl.active, empl.promotor))
            cursor.execute('SELECT LASTVAL()')
            eid = cursor.fetchone()[0]
            empl.id = eid
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
        try:
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
        except:
            self.dbconnect.rollback()
            raise Exception('unable to filter employees')

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
            if employee.id == None:
                raise Exception('no id given')
            cursor.execute('select * from employee where employeeID=%s', (str(employee.id),))
            if cursor.rowcount == 0:
                raise Exception('no employee found with that id')
            cursor.execute(
                'update employee set name= %s,email= %s,office= %s,title= %s,INTernORextern= %s,active= %s,promotor= %s where employeeID=%s',
                (employee.name, employee.email, employee.office, employee.title,
                 employee.internOrExtern, employee.active, employee.promotor, employee.id))
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
