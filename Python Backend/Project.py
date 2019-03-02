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
    def __init__(self,id, title, max_students, research_group, active_year, type, tag,
                 related_project, description,):
        """
        constructor for a dbProject with all variables given
        :param title: a string representing a title
        :param max_students:  an int representing the max amount of students on this project
        :param description: a projectdocument object list that are all the langueages this project supports
        :param research_group: the id of the researchgroup connected with this project (string)
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
        self.ID = id
        self.relatedProject = related_project

    def __str__(self):
        return "title: "+self.title+", max students: "+str(self.maxStudents)+", description"+self.desc+", group: "+self.researchGroup+", year: "+self.activeYear+", type: "+self.type+", tag: "+self.tag+", id: "+str(self.ID)+", related project: "+self.relatedProject
