
CREATE DOMAIN subject as TEXT
  CHECK ( value = 'Computer Science' or value = 'Mathematics' or value = 'Engeneering');

CREATE DOMAIN title as TEXT
  check (value = 'professor' or value = 'phd' or value ='geen');

CREATE DOMAIN intext as TEXT
  check (value = 'intern' or value = 'extern');

CREATE DOMAIN typeResearch as TEXT
  check (value = 'Master thesis' or value =  'Research internship');

CREATE DOMAIN registration as TEXT
  check (value = 'bezig' or value =  'geslaagd' or value = 'niet geslaagd');

CREATE DOMAIN language as TEXT
  check (value='nederlands' or value='engels');

CREATE TABLE document(
  documentID SERIAL PRIMARY key ,
  content text
);

CREATE TABLE researchGroup(
  --needs logo (200x50)
  groupID SERIAL PRIMARY KEY ,
  name varchar(255) unique ,
  abbreviation varchar(25) unique ,
  discipline subject,
  active boolean,     --1 is active, 0 is not active
  adress varchar(255),
  telNr varchar(255) ,
  groupDescription int,
  foreign key (groupDescription) references document (documentID)
  );

create table employee(
  --needs picture (150x150)
  employeeID SERIAL PRIMARY KEY ,
  name varchar,
  email varchar(255) unique,
  office varchar(255), --thinking office is like 'M.G.005'
  researchgroup int references researchGroup(groupID),
  title title,
  internORextern intext,
  active boolean  --1 is active 0 is inactive
);

create table project(
  projectID SERIAL PRIMARY KEY ,
  title varchar(255) not null ,
  maxStudents INT NOT NULL,
  researchGroup int references researchGroup(groupID),
  activeYear int check(activeYear<2100 and activeYear>1970) NOT NULL, --random years within realm of possibilities
  type typeResearch,
  tag varchar,  --e.g. "Databases" later list with possible things
  relatedProject int references project(projectID)
);

create table projectDocument(
  projectID int references project(projectID),
  lang language,
  docID int references document(documentID),
  PRIMARY KEY (projectID,lang)
);

create table session(
  sessionID int PRIMARY KEY ,
  startTime timestamp,
  searchword varchar,
  searchwordtime time,
  clickedProject int references project(projectID),
  clickedProjectTime time
);

create table student(
  studentID SERIAL primary key,
  name varchar(70) NOT NULL ,
  session int references session(sessionID)
);

--registration was suggested to be within student but seemed easier as own entity
create table projectRegistration(
  project int references project(projectID),
  status registration,
  student int references student(studentID),
  PRIMARY KEY (project, status, student)
);

create table bookmark(
  project int references project(projectID),
  student int references student(studentID),
  primary key(project,student)
);