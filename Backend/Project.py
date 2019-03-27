class Project:
    # ik weet niet of deze init nog gebruikt wordt
    # def __init__(self,id, title, max_students, research_group, active_year, type, tag,
    #              related_project, description):
    #     """
    #     constructor for a dbProject with all variables given
    #     :param title: a string representing a title
    #     :param max_students:  an int representing the max amount of students on this project
    #     :param description: the documents object list that are all the langueages this project supports
    #     :param research_group: the id of the researchgroup connected with this project (string)
    #     :param active_year: the year it is active (int)
    #     :param type: a typeResearch enum that says which type of research it is
    #     :param tag: a string that will later do things
    #     :param project_id: a int that is the id of this project
    #     :param related_project: the id of a possible related project
    #     :return:
    #     """
    #     self.title = title
    #     self.maxStudents = max_students
    #     self.desc = description
    #     self.researchGroup = research_group
    #     self.activeYear = active_year
    #     self.type = type
    #     self.tag = tag
    #     self.ID = id
    #     self.relatedProject = related_project
    #     self.promotor=list()

    def __init__(self, id, title, max_students, active, research_group):
        self.title = title
        self.maxStudents = max_students
        self.desc = list()
        self.researchGroup = research_group
        self.active = active
        self.activeYear = list()
        self.type = list()
        self.tag = list()
        self.ID = id
        self.relatedProject = list()
        self.promotor = list()
        self.discipline = list()
        self.registeredStudents = 0

    def get_researchGroup(self, dbConnect):
        access = __import__('DataAccess', fromlist=['ResearchGroupAccess'])
        res = access.ResearchGroupAccess(dbConnect)
        return res.get_researchGroupOnID(self.researchGroup)
