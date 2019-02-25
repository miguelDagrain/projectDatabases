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


class title(Enum):
    geen = 0
    professor = 1
    PHD = 2


class intext(Enum):
    Undefined = 0
    Intern = 1
    Extern = 2


class dbEmployee:
    def __init__(self, email, office, researchgroup, title, interextern, active):
        """
        constructor for dbEmployee  where all varibales are given
        :param email: a string representing an email
        :param office: a string representing a office(building+floor+room)
        :param researchgroup:a string representing a researchgroup (must represent the name of a dbResearch=gorup)
        :param title: a title enum
        :param interextern:  a intext enum
        :param active: a bool stating whether the employee is active or not
        :return: a new dbEmployee object
        """
        self.m_email = email
        self.m_office = office
        self.m_researchgroup = researchgroup
        self.m_title = title
        self.m_internOrExtern = interextern
        self.m_active = active
