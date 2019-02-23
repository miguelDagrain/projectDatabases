
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

CREATE TABLE document(
  content text unique
);

CREATE TABLE researchGroup(
  --needs logo (200x50)
  name varchar(255) unique ,
  abbreviation varchar(25) unique ,
  discipline subject,
  active bit,     --1 is active, 0 is not active
  adress varchar(255),
  telNr varchar(255) ,
  groupDescription text,
  foreign key (groupDescription) references document (content),
  primary key (name, abbreviation)
  );

create table employee(
  --needs picture (150x150)
  name varchar,
  email varchar(255) unique,
  office varchar(255), --thinking office is like 'M.G.005'
  researchgroup varchar(255) references researchGroup(name),
  title title,
  internORextern intext,
  active bit,  --1 is active 0 is inactive
  PRIMARY KEY(email)
);

create table project(
  title varchar(255) not null ,
  maxStudents INT NOT NULL,
  description text references document(content),
  researchGroup varchar(255) references researchGroup(name),
  activeYear int check(activeYear<2100 and activeYear>1970) NOT NULL, --random years within realm of possibilities
  type typeResearch,
  tag varchar,  --e.g. "Databases" later list with possible things
  projectID int not null UNIQUE PRIMARY KEY,
  relatedProject int references project(projectID)
);

create table session(
  sessionID int unique not null,
  startTime timestamp,
  searchword varchar,
  searchwordtime time,
  clickedProject int references project(projectID),
  clickedProjectTime time
);

create table student(
  name varchar(70) NOT NULL ,
  studentID int not null unique primary key,
  likedProject int references project(projectID),
  session int references session(sessionID)
);

--registration was suggested to be within student but seemed easier as own entity
create table projectRegistration(
  project int references project(projectID),
  status registration,
  student int references student(studentID),
  PRIMARY KEY (project, status, student)
);
