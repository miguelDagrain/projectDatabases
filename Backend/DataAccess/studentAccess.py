import dbConnection

from DataAccess.projectAccess import ProjectAccess


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
        try:
            cursor = self.dbconnect.get_cursor()
            cursor.execute('select * from bookmark where project=%s and student=%s', (projectId, studentId))
            if cursor.rowcount == 0:
                cursor.execute('insert into bookmark values(%s,%s)', (projectId, studentId))
                self.dbconnect.commit()
        except:
            self.dbconnect.rollback()
            raise Exception('unable to add bookmark')

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
        if (cursor.rowcount == 0): return None
        row = cursor.fetchone()
        stu = Student(row[0], row[1], row[2])
        stu.likedProject = self.get_studentBookmarkProject(stu.studentID)
        return stu

    def get_studentOnStudentNumber(self, number):
        """
        gets a single student based of an id
        :param ID: the id of this student
        :return: a single student
        """
        from Student import Student
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT * FROM student WHERE studentnumber=%s ', (number,))
        if (cursor.rowcount != 0):
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
            if stu.studentID is not None:
                cursor.execute('INSERT INTO student values(%s,%s,%s)',
                               (stu.studentID, stu.name, stu.studentNumber))
            else:
                cursor.execute('INSERT INTO student values(default,%s,%s)',
                               (stu.name, stu.studentNumber))
                cursor.execute('select lastval()')
                stu.studentID = cursor.fetchone()[0]
            for i in stu.likedProject:
                self.add_bookmark(i.ID, stu.studentID)

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

    def add_projectRegistration(self, pr, student):
        """
        adds a new projecctregistration
        :param pr: the project
        :param student: the studentId
        """
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO projectRegistration values(%s,%s,%s)',
                           (pr, 'busy', student))
            # get id and return updated object
            self.dbconnect.commit()
        except Exception as e:
            print(e)
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