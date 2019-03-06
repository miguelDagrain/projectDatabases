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


class Subject(Enum):
    Undefined = 0
    ComputerScience = 1
    Mathematics = 2
    Engineering = 3


class ResearchGroup:
    def __init__(self,id, name, abbreviation, discipline, active, address, telephone, desc):
        """
        constructor for a dbResearchGroup
        :param name: a string representing a name for the researchGroup
        :param abbreviation: a string that is an abbreviation for the researchgorup
        :param discipline: a subject Enum that says which discipline this group belongs to
        :param active: a bool saying if the group is active or not
        :param address: a string that is an adress for the group
        :param telephone: a string that is the phone number for the group
        :param desc: an all the documents that are this groups descriptions
        :return:a new dbResearchGroup object
        """
        self.ID=id
        self.name = name
        self.abbreviation = abbreviation
        self.discipline = discipline
        self.active = active
        self.address = address
        self.telNr = telephone
        self.desc = desc
        self.contactID=None

    def __str__(self):
        return "name: "+self.name+", abbreviation: "+self.abbreviation+", discipline: "+self.discipline+\
               ", active: "+str(self.active)+", address: "+self.address+", telNr: "+self.telNr+", desc: "+self.desc
