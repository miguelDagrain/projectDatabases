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


class ResearchType(Enum):
    UNDEFINED = 0
    MASTER_THESIS = 1
    RESEARCH_INTERNSHIP = 2


class Project:
    def __init__(self, title, max_students, description, research_group, active_year, type, tag, project_id,
                 related_project):
        """
        constructor for a dbProject with all variables given
        :param title: a string representing a title
        :param max_students:  an int representing the max amount of students on this project
        :param description: a string that is the description of this project
        :param research_group: the name of the researchgroup connected with this project (string)
        :param active_year: the year it is active (int)
        :param type: a typeResearch enum that says which type of research it is
        :param tag: a string that will later do things
        :param project_id: a int that is the id of this project
        :param related_project: the id of a possible related project
        :return:
        """
        self.title = title
        self.maxStudents = max_students
        self.desc = description
        self.researchGroup = research_group
        self.activeYear = active_year
        self.type = type
        self.tag = tag
        self.projectId = project_id
        self.relatedProject = related_project
