class Bookmark:
    def __init__(self,pid,sid):
        self.project=pid
        self.student=sid

    # def getProject(self,dbconnect):
    #     pro=ProjectAccess(dbconnect)
    #     return pro.get_project(self.project)
    #
    # def getStudent(self,dbconnect):
    #     stu=StudentAccess(dbconnect)
    #     return stu.get_student(self.student)
