DROP DOMAIN IF EXISTS subject CASCADE;
CREATE DOMAIN subject as TEXT
  CHECK ( value = 'Computer Science' or value = 'Mathematics' or value = 'Engeneering');

DROP DOMAIN IF EXISTS title CASCADE ;
CREATE DOMAIN title as TEXT
  check (value = 'professor' or value = 'phd' or value = 'geen');

DROP DOMAIN IF EXISTS intext CASCADE;
CREATE DOMAIN intext as TEXT
  check (value = 'intern' or value = 'extern');

DROP DOMAIN IF EXISTS typeResearch CASCADE;
CREATE DOMAIN typeResearch as TEXT
  check (value = 'Master thesis' or value = 'Research internship');

DROP DOMAIN IF EXISTS registration CASCADE;
CREATE DOMAIN registration as TEXT
  check (value = 'bezig' or value = 'geslaagd' or value = 'niet geslaagd');

DROP DOMAIN IF EXISTS language CASCADE;
CREATE DOMAIN language as TEXT
  check (value = 'nederlands' or value = 'engels');

DROP TABLE IF EXISTS document CASCADE;
CREATE TABLE document
(
  documentID SERIAL PRIMARY key,
  lang       language,
  content    text
);

--dont yet know what the attachment should be so this is placeholder
drop table if exists attachment cascade ;
create table attachment
(
  doc int references document(documentID),
  attachment varchar(255),
  primary key(doc,attachment)
);

DROP TABLE IF EXISTS researchGroup CASCADE;
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

DROP TABLE IF EXISTS groupDescription CASCADE;
CREATE TABLE groupDescription
(
  groupID int references researchGroup (groupID),
  docID   int references document (documentID),
  primary key (groupID, docID)
);

DROP TABLE IF EXISTS employee CASCADE;
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

drop table if exists conctactPerson cascade ;
create table contactPerson(
  employee int references employee(employeeID),
  rgroup int references researchGroup(groupID),
  primary key(employee,rgroup)
);

DROP TABLE IF EXISTS project CASCADE;
CREATE TABLE project
(
  projectID      SERIAL PRIMARY KEY,
  title          varchar(255)                                        not null,
  maxStudents    INT                                                 NOT NULL,
  active boolean,
  researchGroup  int references researchGroup (groupID),
  relatedProject int references project (projectID)
);

drop table if exists projectYear cascade ;
create table projectYear
(
  yearID serial primary key,
  year int check (activeYear < 2100 and activeYear > 1970) not null
);

create table projectYearConnection
(
  yearID int references projectYear(yearID),
  projectID int references project(projectID),
  primary key (yearID,projectID)
);

create table projectType
(
   typeID serial primary key,
   type   typeResearch not null
);

create table projectTypeConnection
(
  typeID int references projectType(type),
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
  project int references project(projectID)
  tag varchar(255),
  primary key(project,tag)
);

create table projectRelation
(
 project1 int references project(projectID),
 project2 int references project(projectID),
 primary key(project1,project2)
);

DROP TABLE IF EXISTS projectDocument CASCADE;
CREATE TABLE projectDocument
(
  projectID int references project (projectID),
  docID     int references document (documentID),
  PRIMARY KEY (projectID, docID)
);



DROP TABLE IF EXISTS student CASCADE;
CREATE TABLE student
(
  studentID SERIAL primary key,
  name      varchar(70) NOT NULL
);

--registration was suggested to be within student but seemed easier as own entity
DROP TABLE IF EXISTS projectRegistration CASCADE;
CREATE TABLE projectRegistration
(
  project int references project (projectID),
  status  registration,
  student int references student (studentID),
  PRIMARY KEY (project, status, student)
);

DROP TABLE IF EXISTS bookmark CASCADE;
CREATE TABLE bookmark
(
  project int references project (projectID),
  student int references student (studentID),
  primary key (project, student)
);

DROP TABLE IF EXISTS session CASCADE;
CREATE TABLE session
(
  sessionID          int PRIMARY KEY,
  studentID          int references student(studentID) not null,
  startTime          timestamp,
  startDate          date
);

create table sessionSearchQuery
(
  sessionID references session(sessionID),
  term VARCHAR(255),
  searchTime timestamp ,
  primary key(sessionID,term,searchTime)
);

create table sessionProjectClick
(
 sessionID references session(sessionID),
  project int references project(projectID),
  searchTime timestamp ,
  primary key(sessionID,project,searchTime)
);



