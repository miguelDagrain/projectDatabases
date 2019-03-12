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
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS contactPerson;
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


-- CREATE DOMAIN SUBJECT as TEXT
--   CHECK ( value = 'Computer Science' or value = 'Mathematics' or value = 'Engineering');

-- CREATE DOMAIN title as TEXT
--   check (value = 'professor' or value = 'phd' or value = 'geen');

-- CREATE DOMAIN INTEXT as TEXT
--   check (value = 'intern' or value = 'extern');

-- CREATE DOMAIN typeResearch as TEXT
--   check (value = 'Master thesis' or value = 'Research internship');

-- CREATE DOMAIN registration as TEXT
--   check (value = 'bezig' or value = 'geslaagd' or value = 'niet geslaagd');

-- CREATE DOMAIN language as TEXT
--   check (value = 'nederlands' or value = 'engels');
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
  doc        INT REFERENCES document (documentID),
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
  groupID INT REFERENCES researchGroup (groupID),
  docID   INT REFERENCES document (documentID),
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

CREATE TABLE contactPerson
(
  employee INT REFERENCES employee (employeeID),
  rgroup   INT REFERENCES researchGroup (groupID) UNIQUE,
  PRIMARY KEY (rgroup)
);

CREATE TABLE project
(
  projectID     SERIAL PRIMARY KEY,
  title         VARCHAR(255) NOT NULL,
  maxStudents   INT          NOT NULL,
  active        BOOLEAN,
  researchGroup INT REFERENCES researchGroup (groupID)
);

CREATE TABLE projectYear
(
  year INT check (Year < 2100 and Year > 1970) NOT NULL PRIMARY KEY
);

CREATE TABLE projectYearConnection
(
  year      INT REFERENCES projectYear (year),
  projectID INT REFERENCES project (projectID),
  PRIMARY KEY (year, projectID)
);

CREATE TABLE projectType
(
  type varchar(255) PRIMARY KEY
);
insert into projectType values ('Master thesis');
insert into projectType values ('Research internship');

CREATE TABLE projectTypeConnection
(
  type      varchar(255) REFERENCES projectType (type),
  projectID INT REFERENCES project (projectID),
  PRIMARY KEY (type, projectId)
);

CREATE TABLE projectPromotor
(
  employee INT REFERENCES employee (employeeID),
  project  INT REFERENCES project (projectID),
  PRIMARY KEY (employee, project)
);

CREATE TABLE projectTag
(
  tag     VARCHAR(255),
  project INT REFERENCES project (projectID),
  PRIMARY KEY (project, tag)
);

CREATE TABLE projectRelation
(
  project1 INT REFERENCES project (projectID),
  project2 INT REFERENCES project (projectID),
  PRIMARY KEY (project1, project2)
);

CREATE TABLE projectDocument
(
  projectID INT REFERENCES project (projectID),
  docID     INT REFERENCES document (documentID),
  PRIMARY KEY (projectID, docID)
);

CREATE TABLE student
(
  studentID SERIAL PRIMARY KEY,
  name      VARCHAR(70) NOT NULL
);

CREATE TABLE projectRegistration
(
  project INT REFERENCES project (projectID),
  status  varchar(255) references registration(status),
  student INT REFERENCES student (studentID),
  PRIMARY KEY (project, status, student)
);

CREATE TABLE bookmark
(
  project INT REFERENCES project (projectID),
  student INT REFERENCES student (studentID),
  PRIMARY KEY (project, student)
);

CREATE TABLE session
(
  sessionID INT PRIMARY KEY,
  studentID INT REFERENCES student (studentID) NOT NULL,
  startTime TIME,
  startDate DATE
);

CREATE TABLE sessionSearchQuery
(
  sessionID  INT REFERENCES session (sessionID),
  term       VARCHAR(255),
  searchTime TIME,
  PRIMARY KEY (sessionID, term, searchTime)
);

CREATE TABLE sessionProjectClick
(
  sessionID  INT REFERENCES session (sessionID),
  project    INT REFERENCES project (projectID),
  searchTime TIME,
  PRIMARY KEY (sessionID, project, searchTime)
);