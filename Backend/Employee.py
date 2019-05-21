class Employee:
    def __init__(self, id, name, email, office, research_group, title, interextern, active, promotor):
        """
        constructor for dbEmployee  where all varibales are given
        :param email: a string representing an email
        :param office: a string representing a office(building+floor+room)
        :param research_group:a string representing a researchgroup (must represent the name of a dbResearch=group)
        :param title: a title enum
        :param interextern:  a Intext enum
        :param active: a bool stating whether the employee is active or not
        :param promotor: a bool stating whtether the employee is a promotor or not
        :return: a new dbEmployee object
        """
        self.id = id
        self.name = name
        self.email = email
        self.office = office
        self.research_group = research_group
        self.title = title
        self.internOrExtern = interextern
        self.active = active
        self.promotor = promotor

    def getResearchGroup(self):
        from DataAccess.researchGroupAccess import ResearchGroupAccess
        res = ResearchGroupAccess()
        return res.get_singleResearchGroupOnID(self.research_group)

    #controleert of employee aanwezig is in database
    def getEmpl(self):
        from DataAccess.employeeAccess import EmployeeAccess
        emp = EmployeeAccess()
        return emp.get_employee(self.id)

    def getProjects(self):
        from DataAccess.employeeAccess import EmployeeAccess
        promotor = EmployeeAccess()
        return promotor.get_employeeProjects(self.id)
