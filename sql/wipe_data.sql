
delete from sessionProjectClick;
delete from sessionSearchQuery;
delete from session;
delete from bookmark;
delete from projectregistration;
delete from student;
delete from projectDocument;
delete from projectRelation;
delete from projectTag;
delete from projectPromotor;
delete from projectTypeConnection;
delete from projectType;
delete from projectYearConnection;
delete from projectYear;
delete from project;
delete from contactPerson;
delete from employee;
delete from groupDescription;
delete from researchGroup;
delete from attachment;
delete from document;

ALTER SEQUENCE document_documentID_seq RESTART 1;
ALTER SEQUENCE researchGroup_groupID_seq RESTART 1;
ALTER SEQUENCE employee_employeeID_seq RESTART 1;
ALTER SEQUENCE project_projectID_seq RESTART 1;
alter sequence projectType_typeID_seq restart 1;
ALTER SEQUENCE student_studentID_seq RESTART 1;

