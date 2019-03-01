# create table employee(
#   --needs picture (150x150)
#   name varchar,
#   email varchar(255) unique,
#   office varchar(255), --thinking office is like 'M.G.005'
#   researchgroup varchar(255) references researchGroup(name),
#   title title,
#   internORextern intext,
#   active bit,  --1 is active 0 is inactive
#   PRIMARY KEY(email)
# );

from enum import Enum


class Title(Enum):
    none = 0
    professor = 1
    PHD = 2


class InText(Enum):
    Undefined = 0
    Intern = 1
    Extern = 2


class Employee:
    def __init__(self, email, office, research_group, title, interextern, active):
        """
        constructor for dbEmployee  where all varibales are given
        :param email: a string representing an email
        :param office: a string representing a office(building+floor+room)
        :param research_group:a string representing a researchgroup (must represent the name of a dbResearch=gorup)
        :param title: a title enum
        :param interextern:  a Intext enum
        :param active: a bool stating whether the employee is active or not
        :return: a new dbEmployee object
        """
        self.email = email
        self.office = office
        self.research_group = research_group
        self.title = title
        self.internOrExtern = interextern
        self.active = active

    def __str__(self):
        return "email: "+self.email+", office: "+self.office+", group: "+self.research_group+", title: "+self.title+", isintern:"+str(self.internOrExtern)+", active: "+str(self.active)