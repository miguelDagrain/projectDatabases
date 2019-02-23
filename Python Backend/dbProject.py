# create table project(
#   title varchar(255) not null ,
#   maxStudents INT NOT NULL,
#   description text references document(content),
#   researchGroup varchar(255) references researchGroup(name),
#   activeYear int check(activeYear<2100 and activeYear>1970) NOT NULL, --random years within realm of possibilities
#   type typeResearch,
#   tag varchar,  --e.g. "Databases" later list with possible things
#   projectID int not null UNIQUE PRIMARY KEY,
#   relatedProject int references project(projectID)
# );

from enum import Enum


class typeResearch(Enum):
    Undefined = 0
    MasterThesis = 1
    researchInternship = 2


class dbProject:
    m_title = None
    m_maxStudents = None
    m_description = None
    m_researchGroup = None
    m_activeyear = None
    m_type = None
    m_tag = None
    m_projectId = None
    m_relatedProject = None

    def dbProject(self, title, maxStudents, description, researchgroup, activeyear, type, tag, projectId,
                  relatedproject):
        """
        constructor for a dbProject with all variables given
        :param title: a string representing a title
        :param maxStudents:  an int representing the max amount of students on this project
        :param description: a string that is the description of this project
        :param researchgroup: the name of the researchgroup connected with this project (string)
        :param activeyear: the year it is active (int)
        :param type: a typeResearch enum that says which type of research it is
        :param tag: a string that will later do things
        :param projectId: a int that is the id of this project
        :param relatedproject: the id of a possible related project
        :return:
        """
        self.m_title = title
        self.m_maxStudents = maxStudents
        self.m_description = description
        self.m_researchGroup = researchgroup
        self.m_activeyear = activeyear
        self.m_type = type
        self.m_tag = tag
        self.m_projectId = projectId
        self.m_relatedProject = relatedproject
