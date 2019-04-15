DROP TABLE IF EXISTS sessionProjectClick;
DROP TABLE IF EXISTS sessionSearchQuery;
DROP TABLE IF EXISTS session CASCADE;
DROP TABLE IF EXISTS bookmark;
DROP TABLE IF EXISTS projectRegistration;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS projectDocument;
DROP TABLE IF EXISTS projectRelation;
DROP TABLE IF EXISTS projectTag;
DROP TABLE IF EXISTS projectPromotor;
DROP TABLE IF EXISTS projectTypeConnection;
DROP TABLE IF EXISTS projectType;
DROP TABLE IF EXISTS projectYearConnection;
DROP TABLE IF EXISTS projectYear;
drop table if exists projectResearchgroup;
drop table if exists projectDiscipline;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS contactPerson;
DROP TABLE IF EXISTS employeeRoles;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS groupDescription;
DROP TABLE IF EXISTS researchGroup;
DROP TABLE IF EXISTS attachment;
DROP TABLE IF EXISTS document;
drop table if exists discipline;
drop table if exists language;
drop table if exists title;
drop table if exists intext;
drop table if exists typeResearch;
drop table if exists registration;
DROP DOMAIN IF EXISTS language;
DROP DOMAIN IF EXISTS registration;
DROP DOMAIN IF EXISTS typeResearch;
DROP DOMAIN IF EXISTS INTEXT;
DROP DOMAIN IF EXISTS title;
DROP DOMAIN IF EXISTS subject;

create table title(
  title varchar(255) primary key
);
insert into title values('professor');
insert into title values('phd');
insert into title values('none');

create table intext(
  origin varchar(255) primary key
);
insert into intext values ('intern');
insert into intext values ('extern');

create table registration(
  status varchar(255) primary key
);
insert into registration values ('busy');
insert into registration values ('succeeded');
insert into registration values ('failed');

create table language(
  lang varchar(255) primary key
);
insert into language values ('dutch');
insert into language values ('english');


create table discipline
(
  subject varchar(255) primary key
);
insert into discipline values('Computer Science');
insert into discipline values('Mathematics');
insert into discipline values('Engineering');

CREATE TABLE document
(
  documentID SERIAL PRIMARY KEY,
  lang    varchar(255) references language(lang),
  content    text
);

--dont yet know what the attachment should be so this is placeholder
CREATE TABLE attachment
(
  doc        INT REFERENCES document (documentID) ON DELETE CASCADE,
  attachment VARCHAR(255),
  PRIMARY KEY (doc, attachment)
);

CREATE TABLE researchGroup
(
  --needs logo (200x50)
  groupID      SERIAL PRIMARY KEY,
  name         VARCHAR(255) UNIQUE,
  abbreviation VARCHAR(25) UNIQUE,
  discipline   varchar(255) references discipline(subject),
  active       BOOLEAN, --1 is active, 0 is not active
  address      VARCHAR(255),
  telNr        VARCHAR(255)
);


CREATE TABLE groupDescription
(
  groupID INT REFERENCES researchGroup (groupID) ON DELETE CASCADE ,
  docID   INT REFERENCES document (documentID) ON DELETE CASCADE ,
  PRIMARY KEY (groupID, docID)
);

CREATE TABLE employee
(
  --needs picture (150x150)
  employeeID     SERIAL PRIMARY KEY,
  name           VARCHAR,
  email          VARCHAR(255) UNIQUE,
  office         VARCHAR(255), --thinking office is like 'M.G.005'
  researchgroup  INT REFERENCES researchGroup (groupID),
  title          varchar(255) references title(title),
  INTernORextern varchar(255) references intext(origin),
  active         BOOLEAN,
  promotor       BOOLEAN

);

create table employeeRoles
(
  employee int references employee (employeeID) ON DELETE CASCADE,
  role     varchar(255),
  primary key (role, employee)
);

CREATE TABLE contactPerson
(
  employee INT REFERENCES employee (employeeID) ON DELETE CASCADE,
  rgroup   INT REFERENCES researchGroup (groupID) UNIQUE,
  PRIMARY KEY (rgroup)
);

CREATE TABLE project
(
  projectID     SERIAL PRIMARY KEY,
  title         VARCHAR(255) NOT NULL,
  maxStudents   INT          NOT NULL,
  active        BOOLEAN
);

CREATE TABLE projectDiscipline
(
  projectID int references project(projectID) ON DELETE CASCADE,
  discipline varchar(255) references discipline(subject),
  primary key (projectID, discipline)
);

create table projectResearchgroup
(
  projectID int references project(projectID) ON DELETE CASCADE,
  researchgroupid int references researchGroup(groupID),
  primary key (projectid,researchgroupid)
);

CREATE TABLE projectYear
(
  year INT check (Year < 2100 and Year > 1970) NOT NULL PRIMARY KEY
);

CREATE TABLE projectYearConnection
(
  year      INT REFERENCES projectYear (year),
  projectID INT REFERENCES project (projectID) ON DELETE CASCADE,
  PRIMARY KEY (year, projectID)
);

CREATE TABLE projectType
(
  type varchar(255) PRIMARY KEY
);
insert into projectType values ('Master thesis');
insert into projectType values ('Research internship 2');
insert into projectType values ('Research internship 1');
insert into projectType values ('Bachelor dissertation');

CREATE TABLE projectTypeConnection
(
  type      varchar(255) REFERENCES projectType (type),
  projectID INT REFERENCES project (projectID) ON DELETE CASCADE ,
  PRIMARY KEY (type, projectId)
);

CREATE TABLE projectPromotor
(
  employee INT REFERENCES employee (employeeID) ON DELETE CASCADE,
  project  INT REFERENCES project (projectID) ON DELETE CASCADE,
  PRIMARY KEY (employee, project)
);

CREATE TABLE projectTag
(
  tag     VARCHAR(255),
  project INT REFERENCES project (projectID) ON DELETE CASCADE,
  PRIMARY KEY (project, tag)
);

CREATE TABLE projectRelation
(
  project1 INT REFERENCES project (projectID) ON DELETE CASCADE,
  project2 INT REFERENCES project (projectID) ON DELETE CASCADE,
  PRIMARY KEY (project1, project2)
);

CREATE TABLE projectDocument
(
  projectID INT REFERENCES project (projectID), -- On delete cascade is niet nodig omwille van de trigger
  docID     INT REFERENCES document (documentID) ON DELETE CASCADE,
  PRIMARY KEY (projectID, docID)
);

CREATE TABLE student
(
  studentID SERIAL PRIMARY KEY,
  name      VARCHAR(70) NOT NULL,
  studentnumber int NOT NULL
);

CREATE TABLE projectRegistration
(
  project INT REFERENCES project (projectID) ON DELETE CASCADE,
  status  varchar(255) references registration(status),
  student INT REFERENCES student (studentID),
  PRIMARY KEY (project, status, student)
);

CREATE TABLE bookmark
(
  project INT REFERENCES project (projectID) ON DELETE CASCADE,
  student INT REFERENCES student (studentID) ON DELETE CASCADE,
  PRIMARY KEY (project, student)
);

drop function if exists researchGroup_del_func;
 CREATE FUNCTION researchGroup_del_func() RETURNS trigger AS $action$
 BEGIN
     UPDATE employee
     SET researchgroup = 1
     WHERE researchgroup = old.groupID;


     UPDATE projectResearchgroup
     SET researchgroupid = 1
     WHERE researchgroupid = old.groupID;

     DELETE FROM document
      WHERE documentID = (SELECT docID
                        FROM groupDescription NATURAL JOIN researchGroup rG
                        WHERE rG.groupID = old.groupID);

     RETURN old;
 END
 $action$ LANGUAGE plpgsql;

drop trigger if exists researchGroup_del_tr ON researchGroup;
CREATE TRIGGER researchGroup_del_tr
BEFORE DELETE ON researchGroup
FOR EACH ROW
WHEN (old.groupID <> 1)
EXECUTE PROCEDURE researchGroup_del_func();

drop function if exists project_del_func;
 CREATE FUNCTION project_del_func() RETURNS trigger AS $action$
 BEGIN

   DELETE FROM document
   WHERE documentID = (SELECT docID
                       FROM projectDocument
                       WHERE projectID = old.projectID);

   RETURN old;

 END
 $action$ LANGUAGE plpgsql;

drop trigger if exists project_del_tr on project;
CREATE TRIGGER project_del_tr
BEFORE DELETE ON project
FOR EACH ROW
EXECUTE PROCEDURE project_del_func();