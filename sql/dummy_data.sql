INSERT into document values(default ,'dutch','ik ben jos het document');
insert into document values(default ,'dutch','wij zijn een groep');
insert into document values(default ,'dutch','vandaag is de dag dat de wereld samenkomt en eindelijk belgie wat groter maakt');
insert into document values(default ,'english','today is the day the world unites and finally makes belgium a bit bigger');

insert into attachment values(1,'jos heeft ook een attachment');
insert into attachment values(1,'jos heeft zelfs 2 attachments');
insert into attachment values(2,'de groep heeft ook een attachment');
insert into attachment values(3,'attachments zijn voor losers');

Insert into researchGroup values(default ,'de grote groep','dgr','Computer Science','true','hiere','120725625');

insert into groupDescription values(1,2);

insert into employee values(default,'joske','joske@mailke.com','oppuurseSteenweg 7',1,'none','intern',true,false);

insert into contactPerson values(1,1);

insert into project values(default,'verover nederland',10000,true,1);
insert into project values(default,'verover frankrijk',10000,true,1);

insert into projectYear values(1971);
insert into projectYear values(1972);
insert into projectYear values(1973);

insert into projectYearConnection values(1971,1);
insert into projectYearConnection values(1972,1);
insert into projectYearConnection values(1973,2);

insert into projectTypeConnection values('Master thesis',1);
insert into projectTypeConnection values('Research internship',2);

insert into projectPromotor values(1,1);
insert into projectPromotor values(1,2);

insert into projectTag values('feesten',1);
insert into projectTag values('niet feesten',2);

insert into projectRelation values(1,2);

insert into projectDocument values(1,3);
insert into projectDocument values(2,4);

insert into student values(default,'jefke vande nabelen');

insert into projectRegistration values(1,'busy',1);

insert into bookmark values(1,1);
insert into bookmark values(2,1);

insert into session values(10,1,'12:24:52','2019-04-03');

insert into sessionSearchQuery values(10,'veroveren','12:29:52');
insert into sessionSearchQuery values(10,'nederland','12:31:52');

-- insert into sessionProjectClick values(10,1,'12:29:59');
-- insert into sessionProjectClick values(10,2,'12:31:59');


-- insert into session values(1251,'2011-01-01 00:00:00'::TIMESTAMP,'feest vieren','00:00:00',1,'24:00:00');


