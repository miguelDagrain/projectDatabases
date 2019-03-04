DROP TABLE IF EXISTS sessionProjectClick ;
DROP TABLE IF EXISTS sessionSearchQuery ;
DROP TABLE IF EXISTS session ;
DROP TABLE IF EXISTS bookmark ;
DROP TABLE IF EXISTS projectRegistration ;
DROP TABLE IF EXISTS student ;
DROP TABLE IF EXISTS projectDocument ;
DROP TABLE IF EXISTS projectRelation ;
DROP TABLE IF EXISTS projectTag ;
DROP TABLE IF EXISTS projectPromotor ;
DROP TABLE IF EXISTS projectTypeConnection ;
DROP TABLE IF EXISTS projectType ;
DROP TABLE IF EXISTS projectYearConnection ;
drop table if exists projectYear ;
DROP TABLE IF EXISTS project ;
drop table if exists contactPerson;
DROP TABLE IF EXISTS employee ;
DROP TABLE IF EXISTS groupDescription ;
DROP TABLE IF EXISTS researchGroup ;
drop table if exists attachment ;
DROP TABLE IF EXISTS document ;
DROP DOMAIN IF EXISTS language ;
DROP DOMAIN IF EXISTS registration ;
DROP DOMAIN IF EXISTS typeResearch ;
DROP DOMAIN IF EXISTS intext ;
DROP DOMAIN IF EXISTS title ;
DROP DOMAIN IF EXISTS subject ;


CREATE DOMAIN subject as TEXT
  CHECK ( value = 'Computer Science' or value = 'Mathematics' or value = 'Engeneering');

CREATE DOMAIN title as TEXT
  check (value = 'professor' or value = 'phd' or value = 'geen');

CREATE DOMAIN intext as TEXT
  check (value = 'intern' or value = 'extern');

CREATE DOMAIN typeResearch as TEXT
  check (value = 'Master thesis' or value = 'Research internship');

CREATE DOMAIN registration as TEXT
  check (value = 'bezig' or value = 'geslaagd' or value = 'niet geslaagd');

CREATE DOMAIN language as TEXT
  check (value = 'nederlands' or value = 'engels');

CREATE TABLE document
(
  documentID SERIAL PRIMARY key,
  lang       language,
  content    text
);

--dont yet know what the attachment should be so this is placeholder
create table attachment
(
  doc int references document(documentID),
  attachment varchar(255),
  primary key(doc,attachment)
);

CREATE TABLE researchGroup
(
  --needs logo (200x50)
  groupID      SERIAL PRIMARY KEY,
  name         varchar(255) unique,
  abbreviation varchar(25) unique,
  discipline   subject,
  active       boolean, --1 is active, 0 is not active
  address      varchar(255),
  telNr        varchar(255)
);

CREATE TABLE groupDescription
(
  groupID int references researchGroup (groupID),
  docID   int references document (documentID),
  primary key (groupID, docID)
);

CREATE TABLE employee
(
  --needs picture (150x150)
  employeeID     SERIAL PRIMARY KEY,
  name           varchar,
  email          varchar(255) unique,
  office         varchar(255), --thinking office is like 'M.G.005'
  researchgroup  int references researchGroup (groupID),
  title          title,
  internORextern intext,
  active         boolean,
  promotor       boolean

);

create table contactPerson(
  employee int references employee(employeeID),
  rgroup int references researchGroup(groupID),
  primary key(employee,rgroup)
);

CREATE TABLE project
(
  projectID      SERIAL PRIMARY KEY,
  title          varchar(255)                                        not null,
  maxStudents    INT                                                 NOT NULL,
  active boolean,
  researchGroup  int references researchGroup (groupID)
);

create table projectYear
(
  yearID serial primary key,
  year int check (Year < 2100 and Year > 1970) not null
);

create table projectYearConnection
(
  yearID int references projectYear(yearID),
  projectID int references project(projectID),
  primary key (yearID,projectID)
);

create table projectType
(
   typeID SERIAL unique primary key,
   type   typeResearch not null
);

create table projectTypeConnection
(
  typeID int references projectType(typeID),
  projectID int references project(projectID),
  primary key (typeID,projectId)
);

create table projectPromotor
(
  employee int references employee(employeeID),
  project int references project(projectID),
  primary key (employee,project)
);

create table projectTag
(
  project int references project(projectID),
  tag varchar(255),
  primary key(project,tag)
);

create table projectRelation
(
 project1 int references project(projectID),
 project2 int references project(projectID),
 primary key(project1,project2)
);

CREATE TABLE projectDocument
(
  projectID int references project (projectID),
  docID     int references document (documentID),
  PRIMARY KEY (projectID, docID)
);

CREATE TABLE student
(
  studentID SERIAL primary key,
  name      varchar(70) NOT NULL
);

CREATE TABLE projectRegistration
(
  project int references project (projectID),
  status  registration,
  student int references student (studentID),
  PRIMARY KEY (project, status, student)
);

CREATE TABLE bookmark
(
  project int references project (projectID),
  student int references student (studentID),
  primary key (project, student)
);

CREATE TABLE session
(
  sessionID          int PRIMARY KEY,
  studentID          int references student(studentID) not null,
  startTime          time,
  startDate          date
);

create table sessionSearchQuery
(
  sessionID int references session(sessionID),
  term VARCHAR(255),
  searchTime time ,
  primary key(sessionID,term,searchTime)
);

create table sessionProjectClick
(
  session int references session(sessionID),
  project int references project(projectID),
  searchTime time ,
  primary key(session,project,searchTime)
);