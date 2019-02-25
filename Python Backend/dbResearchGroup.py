# CREATE TABLE researchGroup(
#   --needs logo (200x50)
#   name varchar(255) unique ,
#   abbreviation varchar(25) unique ,
#   discipline subject,
#   active bit,     --1 is active, 0 is not active
#   adress varchar(255),
#   telNr varchar(255) ,
#   groupDescription text,
#   foreign key (groupDescription) references document (content),
#   primary key (name, abbreviation)
#   );

from enum import Enum


class subject(Enum):
    Undefined = 0
    ComputerScience = 1
    Mathemetics = 2
    Engeneering = 3


class dbResearchGroup:
    def __init__(self, name, abbreviation, discipline, active, adress, telNr, groupDescription):
        """
        constructor for a dbResearchGroup
        :param name: a string representing a name for the researchGroup
        :param abbreviation: a string that is an abbreviation for the researchgorup
        :param discipline: a subject Enum that says which discipline this group belongs to
        :param active: a bool saying if the group is active or not
        :param adress: a string that is an adress for the group
        :param telNr: a string that is the phone number for the group
        :param groupDescription: a string that is the full description of the group
        :return:a new dbResearchGroup object
        """
        self.m_name = name
        self.m_abbreviation = abbreviation
        self.m_discipline = discipline
        self.m_active = active
        self.m_adress = adress
        self.m_telNr = telNr
        self.m_groupDescription = groupDescription
