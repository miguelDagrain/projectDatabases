delete from bookmark;
delete from projectregistration;
delete from student;
delete from session;
delete from projectDocument;
delete from project;
delete from employee;
delete from groupdescription;
delete from researchGroup;
delete from document;

ALTER SEQUENCE document_documentID_seq RESTART 1;
ALTER SEQUENCE researchGroup_groupID_seq RESTART 1;
ALTER SEQUENCE employee_employeeID_seq RESTART 1;
ALTER SEQUENCE project_projectID_seq RESTART 1;
ALTER SEQUENCE student_studentID_seq RESTART 1;
