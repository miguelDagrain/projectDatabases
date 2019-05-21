class Bookmark:
    def __init__(self, pid, sid):
        self.project = pid
        self.student = sid

    def getProject(self):
        from DataAccess.projectAccess import ProjectAccess
        pro = ProjectAccess()
        return pro.get_project(self.project)

    def getStudent(self):
        from DataAccess.studentAccess import StudentAccess
        stu = StudentAccess()
        return stu.get_student(self.student)
