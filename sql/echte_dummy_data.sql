insert into document (documentID, lang, content) values (default, 'engels', 'PROTOTYPE XML DOCUMENT SERVER,<p>Contact adres:\n<ul>\n<li>ACUNIA N.V.\n<li>Philips-site 5 box 3\n<li>3001 Leuven\n<li><a href=\"http://www.acunia.be\">Acunia</a>\n</ul>\n<p>\nContext:<br>\nACUNIA is een firma gesticht in 1996, de core business van ACUNIA is de telematica industrie, die telecommunicatie en informatie technologie combineert in mobiele en vaste toestellen. Acunia ontwikkeld ook Wonka<sup>TM</sup>, een cleanroom Virtual Machine voor Java. Wonka<sup>TM</sup> is extreem draagbare en self-contained en kan gebruikt worden in combinatie met zijn eigen RTOS (run-time operation system) om complete oplossingen voor embedded devices aan te bieden. De Wonka VM is Java2 compatibel en de Wonka class libraries bevatten alle classes die nodig zijn om een OSGi framework te ondersteunen.<p>\nACUNIA heeft ook zijn eigen run-time compiler voor Wonka ontwikkeld, die optimalizatie algoritmen zal gebruiken om de performantie van een embedded systeem te verhogen. Het doel van deze stage is te onderzoeken hoe de bestaande algoritmen kunnen uitgebreid worden om meer complexe \"<i>refactoringen</i>\" zoals method inlining te ondersteunen.</p>\n');
insert into document (documentID, lang, content) values (default, 'engels', 'MODELLEREN VAN MPEG-2 VIDEO BRONNEN,<p>Deze thesis handelt over de typische eigenschappen van MPEG-2 video die niet in MPEG-1 zitten. De bedoeling van deze thesis is tweezijdig. Enerzijds bestaat deze uit het onderzoeken van bestaande MPEG- 2 modellen die een of meerdere van die speciale MPEG-2 features modelleren. Op basis hiervan kan dan een nieuw model opgesteld worden dat een aantal modellen combineert. Deze thesis kan eventueel door 2 studenten gedaan worden. Afhankelijk hiervan kan er meer of minder nadruk gelegd worden op de implementatie van oplossingsmethoden.</p>\n');
insert into document (documentID, lang, content) values (default, 'engels', '<p>In een CDN (Content Distribution Network) kan de controle van het\ndistributieproces zowel centraal als gedistribueerd gebeuren.  Bedoeling\nvan deze thesis is om de invloed hiervan op de performantie en signaling\noverhead na te gaan.</p>\n');
insert into document (documentID, lang, content) values (default, 'engels', 'SCHEDULING MECHANISMES VOOR AUDIO EN VIDEO STROMEN,<p>De bedoeling van deze thesis is om te onderzoeken met welke scheduling\nalgoritmes en met welke parameterkeuze voor deze algoritmes de QoS (Quality of Service) voor audio- en videostromen gegarandeerd kan worden, zowel in een knooppunt als end-to-end.</p>\n');
insert into document values(default,'engels','wij hebben geen description');
insert into document values(default,'engels','<p>Contact adres:\n<ul>\n<li>ACUNIA N.V.\n<li>Philips-site 5 box 3\n<li>3001 Leuven\n<li><a href=\"http://www.acunia.be\">Acunia</a>\n</ul>\n<p>\nContext:<br>\nACUNIA is een firma gesticht in 1996, de core business van ACUNIA is de telematica industrie, die telecommunicatie en informatie technologie combineert in mobiele en vaste toestellen. Acunia ontwikkeld ook Wonka<sup>TM</sup>, een cleanroom Virtual Machine voor Java. Wonka<sup>TM</sup> is extreem draagbare en self-contained en kan gebruikt worden in combinatie met zijn eigen RTOS (run-time operation system) om complete oplossingen voor embedded devices aan te bieden. De Wonka VM is Java2 compatibel en de Wonka class libraries bevatten alle classes die nodig zijn om een OSGi framework te ondersteunen.<p>\nACUNIA heeft ook zijn eigen run-time compiler voor Wonka ontwikkeld, die optimalizatie algoritmen zal gebruiken om de performantie van een embedded systeem te verhogen. Het doel van deze stage is te onderzoeken hoe de bestaande algoritmen kunnen uitgebreid worden om meer complexe \"<i>refactoringen</i>\" zoals method inlining te ondersteunen.</p>\n');
insert into document values(default,'engels','<p>Deze thesis handelt over de typische eigenschappen van MPEG-2 video die niet in MPEG-1 zitten. De bedoeling van deze thesis is tweezijdig. Enerzijds bestaat deze uit het onderzoeken van bestaande MPEG- 2 modellen die een of meerdere van die speciale MPEG-2 features modelleren. Op basis hiervan kan dan een nieuw model opgesteld worden dat een aantal modellen combineert. Deze thesis kan eventueel door 2 studenten gedaan worden. Afhankelijk hiervan kan er meer of minder nadruk gelegd worden op de implementatie van oplossingsmethoden.</p>\n');
insert into document values(default,'engels','<p>In een CDN (Content Distribution Network) kan de controle van het\ndistributieproces zowel centraal als gedistribueerd gebeuren.  Bedoeling\nvan deze thesis is om de invloed hiervan op de performantie en signaling\noverhead na te gaan.</p>\n');

insert into attachment values(1,'jos heeft ook een attachment');
insert into attachment values(1,'jos heeft zelfs 2 attachments');
insert into attachment values(2,'de groep heeft ook een attachment');


insert into researchGroup values (default,'No research group','NONE','Computer Science',true,'middelheim','0');
insert into researchGroup values (default,'Modelling of Systems and Internet Communication','MOSAIC','Computer Science',true,'middelheim','0');
insert into researchGroup values (default,'Advanced Database Research and Modelling','ADReM','Computer Science',true,'middelheim','0');
insert into researchGroup values (default,'Lab On REengineering','LORE','Computer Science',true,'middelheim','0');

insert into groupDescription values(1,5);
insert into groupDescription values(2,5);
insert into groupDescription values(3,5);
insert into groupDescription values(4,5);

insert into employee values(default,'Chris Blondia','chris.blondia@uantwerpen.be','oppuurseSteenweg 7',2,'phd','intern',true,true);
insert into employee values(default,'Bart Braem','bart.braem@uantwerpen.be','oppuurseSteenweg 7',2,'phd','intern',true,true);
insert into employee values(default,'Jeroen Avonts','jeroen.avonts@uantwerpen.be','oppuurseSteenweg 7',2,'phd','intern',true,true);
insert into employee values(default,'Johan Bergs','johan.bergs@uantwerpen.be','oppuurseSteenweg 7',2,'phd','intern',true,true);

insert into contactPerson values(2,1);

insert into project values (default,'PROTOTYPE XML DOCUMENT SERVER',1,true,1);
insert into project values (default,'MODELLEREN VAN MPEG-2 VIDEO BRONNEN',2,false,1);
insert into project values (default,'INVLOED VAN HET DISTRIBUTIEPROCES OP DE PERFORMANTIE VAN EEN CDN EN OP DE SIGNALING OVERHEAD',1,false,1);

insert into projectYear values(2019);
insert into projectYear values(2020);
insert into projectYear values(2021);

insert into projectYearConnection values(2019,1);
insert into projectYearConnection values(2020,2);
insert into projectYearConnection values(2021,3);

insert into projectType values('Master thesis');
insert into projectType values('Research internship');

insert into projectTypeConnection values('Master thesis',1);
insert into projectTypeConnection values('Research internship',2);
insert into projectTypeConnection values('Research internship',3);

insert into projectPromotor values(1,1);
insert into projectPromotor values(1,2);
insert into projectPromotor values(1,3);

insert into projectTag values('PROTOTYPE XML DOCUMENT SERVER',1);
insert into projectTag values('MODELLEREN VAN MPEG-2 VIDEO BRONNEN',2);
insert into projectTag values('INVLOED VAN HET DISTRIBUTIEPROCES OP DE PERFORMANTIE VAN EEN CDN EN OP DE SIGNALING OVERHEAD',3);

insert into projectRelation values(1,2);

insert into projectDocument values(1,6);
insert into projectDocument values(2,7);
insert into projectDocument values(2,8);

insert into student values (default,'Van Leuvenhaege Matthias');
insert into student values (default,'Molderez Tim');
insert into student values (default,'Mertens Tim');

insert into projectRegistration values (3,'bezig',1);
insert into projectRegistration values (3,'bezig',2);
insert into projectRegistration values (3,'bezig',3);

insert into bookmark values(1,1);
insert into bookmark values(2,1);

insert into session values(10,1,'12:24:52','2019-04-03');

insert into sessionSearchQuery values(10,'prototype','12:29:52');
insert into sessionSearchQuery values(10,'modeleren','12:31:52');

insert into sessionProjectClick values(10,1,'12:29:59');
insert into sessionProjectClick values(10,2,'12:31:59');


