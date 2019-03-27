class Bookmark:
    def __init__(self, pid, sid):
        self.project = pid
        self.student = sid

    def getProject(self, dbconnect):
        access = __import__('DataAccess', fromlist=['ProjectAccess'])
        pro = access.ProjectAccess(dbconnect)
        return pro.get_project(self.project)

    def getStudent(self, dbconnect):
        access = __import__('DataAccess', fromlist=['StudentAccess'])
        stu = access.StudentAccess(dbconnect)
        return stu.get_student(self.student)
