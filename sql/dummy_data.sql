SET TIMEZONE TO 'JT';
INSERT into document values(default ,'ik ben jos het document');
insert into document values(default ,'wij zijn een groep');
insert into document values(default ,'vandaag is de dag dat de wereld samenkomt en eindelijk belgie wat groter maakt');
insert into document values(default ,'today is the day the world unites and finally makes belgium a bit bigger');
Insert into researchGroup values(default ,'de grote groep','dgr','Computer Science','true','hiere','120725625','1');
insert into employee values(default,'joske','joske@mailke.com','oppuurseSteenweg 7',1,'geen','intern',true);
insert into project values(default,'verover polen',1000000,1,2010,'Master thesis','tag?',null );
insert into projectDocument values(1,'nederlands',3);
insert into projectDocument values(1,'engels',4);
insert into session values(1251,'2011-01-01 00:00:00'::TIMESTAMP,'feest vieren','00:00:00',1,'24:00:00');
insert into student values(default,'jefke vande nabelen',1251);
insert into projectRegistration values(1,'bezig',1);
insert into bookmark values(1,1);

-- insert into document values();
-- insert into document values('wij zijn een groep');
-- Insert into researchGroup values('de grote groep','dgr','Computer Science','true','hiere','120725625','wij zijn een groep');