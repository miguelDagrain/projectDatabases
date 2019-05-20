class Project:
    def __init__(self, id, title, max_students, active):
        self.title = title
        self.maxStudents = max_students
        self.desc = list()
        self.researchGroup = list()
        self.active = active
        self.activeYear = list()
        self.type = list()
        self.tag = list()
        self.ID = id
        self.relatedProject = list()
        self.promotors = list()
        self.supervisors = list()
        self.extern_employees = list()
        self.discipline = list()
        self.registeredStudents = 0
        self.register_count = 0
        self.desc_nl = None
        self.desc_en = None

