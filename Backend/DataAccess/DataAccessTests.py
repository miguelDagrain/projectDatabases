import unittest
from DataAccess import *
import dbConnection
from Document import *
from Attachment import *
from ResearchGroup import *
from Employee import *
from ProjectRegistration import *
from Project import *
from Student import *
from DataAccess.documentAccess import DocumentAccess
from DataAccess.domainAccess import  DomainAccess
from DataAccess.employeeAccess import EmployeeAccess
from DataAccess.projectAccess import ProjectAccess
from DataAccess.researchGroupAccess import ResearchGroupAccess
from DataAccess.sessionAccess import SessionAccess
from DataAccess.studentAccess import StudentAccess




class Test(unittest.TestCase):
    def setupDB(self):
        dbConnection.setConnection('testpdbdatabase','testpdb','test','localhost')
        self.dbconnect=dbConnection.connection
        cursor=self.dbconnect.get_cursor()
        file =open("../sql/ESP.sql", "r")
        cursor.execute(file.read())
        file.close()
    def wipeDB(self):
        cursor = self.dbconnect.get_cursor()
        file = open("../sql/ESP.sql", "r")
        cursor.execute(file.read())
        file.close()

    def test_DomainAcces(self):
        self.setupDB()
        da=DomainAccess()
        di=da.get_disciplines()
        self.assertEqual(3,len(di),"length should be 3 but is:" +str(len(di)))
        da.add_discipline('testdiscipline')
        di = da.get_disciplines()
        self.assertEqual(4, len(di), "length should be 4 but is:" + str(len(di)))
        self.assertEqual('testdiscipline',di[3],'fourth testdiscipline is not testdiscipline')

        io=da.get_intextOrigin()
        self.assertEqual(2,len(io),'length should be 2 but isnt')
        da.add_intextOrigin('intexttest')
        io = da.get_intextOrigin()
        self.assertEqual(3, len(io), "length should be 3 but is:" + str(len(io)))
        self.assertEqual('intexttest', io[2], 'third intextorigin is not testintext')

        ln = da.get_languages()
        self.assertEqual(2, len(ln), 'length of languages should be 2 but isnt')
        da.add_language('langtest')
        ln = da.get_languages()
        self.assertEqual(3, len(ln), "length should be 3 but is:" + str(len(ln)))
        self.assertEqual('langtest', ln[2], 'third language is not langtest')

        tp = da.get_projectType()
        self.assertEqual(4, len(tp), 'length of projectypes should be 4 but isnt')
        da.add_projectType('testtype')
        tp = da.get_projectType()
        self.assertEqual(5, len(tp), "length should be 5 but is:" + str(len(tp)))
        self.assertEqual('testtype', tp[4], 'third projecttype is not testtype')

        rs = da.get_registrationStatus()
        self.assertEqual(3, len(rs), 'length of registrationstatus should be 3 but isnt')
        da.add_registrationStatus('testregistration')
        rs = da.get_registrationStatus()
        self.assertEqual(4, len(rs), "length should be 4 but is:" + str(len(rs)))
        self.assertEqual('testregistration', rs[3], 'third registrationstatus is not testregistration')

        ti = da.get_titles()
        self.assertEqual(3, len(ti), 'length of titles should be 3 but isnt')
        da.add_title('testtitle')
        ti = da.get_titles()
        self.assertEqual(4, len(ti), "length should be 4 but is:" + str(len(ti)))
        self.assertEqual('testtitle', ti[3], 'third title is not testtitle')

    def test_DocumentAcces(self):
        self.setupDB()
        da = DocumentAccess()
        doc=da.get_documents()
        self.assertEqual(0,len(doc))

        newdoc=Document(None,'english','testdoc')
        da.add_document(newdoc)
        doc = da.get_documents()
        self.assertEqual(1, len(doc))
        self.assertEqual(1, doc[0].ID)
        self.assertEqual('english', doc[0].language)
        self.assertEqual('testdoc', doc[0].text)

        newdoc = Document(None, 'dutch', 'testdocer')
        da.add_document(newdoc)
        doc = da.get_documents()
        self.assertEqual(2, len(doc))
        self.assertEqual(2, doc[1].ID)
        self.assertEqual('dutch', doc[1].language)
        self.assertEqual('testdocer', doc[1].text)

        da.add_attachment(1,'testattachment')
        doc = da.get_documents()
        self.assertEqual(2, len(doc))
        self.assertEqual(1, doc[0].ID)
        self.assertEqual('english', doc[0].language)
        self.assertEqual('testdoc', doc[0].text)
        self.assertEqual('testattachment', doc[0].attachment[0].content)

        da.update_document_text(1,"nieuwe tekst")
        doc = da.get_documents()
        self.assertEqual(2, len(doc))
        self.assertEqual(1, doc[1].ID)
        self.assertEqual('english', doc[1].language)
        self.assertEqual('nieuwe tekst', doc[1].text)
        self.assertEqual('testattachment', doc[1].attachment[0].content)

        singledoc=da.get_document(1)
        self.assertEqual(1, singledoc.ID)
        self.assertEqual('english', singledoc.language)
        self.assertEqual('nieuwe tekst', singledoc.text)
        self.assertEqual('testattachment', singledoc.attachment[0].content)

        singledoc.text="nog nieuwere tekst"
        singledoc.language='dutch'
        singledoc.attachment[0].content="nieuwe attachment tekst"
        da.change_Document(singledoc)
        singledoc = da.get_document(1)
        self.assertEqual(1, singledoc.ID)
        self.assertEqual('dutch', singledoc.language)
        self.assertEqual('nog nieuwere tekst', singledoc.text)
        self.assertEqual('nieuwe attachment tekst', singledoc.attachment[0].content)

    def test_researchGroupAccess(self):
        self.setupDB()
        da = DocumentAccess()
        da.add_document(Document(None,'dutch','testgroep'))
        da.add_document(Document(None, 'dutch', 'testergroep'))
        ra = ResearchGroupAccess()

        r =ResearchGroup(None,"testgroep","tg",'Mathematics',True,"hier","0412864523",list())
        ra.add_researchGroup(r)

        r=ra.get_singleResearchGroupOnID(1)
        self.assertEqual("testgroep",r.name)
        self.assertEqual("tg", r.abbreviation)
        self.assertEqual("Mathematics", r.discipline)
        self.assertEqual(True, r.active)
        self.assertEqual("hier", r.address)
        self.assertEqual("0412864523", r.telNr)
        self.assertEqual(0, len(r.desc))

        ra.add_researchGroupDescription(Document(None,'dutch',"testgroepdocument"),1)

        doc=ra.get_researchgroupDescriptions(1)
        self.assertEqual(1,len(doc))
        self.assertEqual("testgroepdocument",doc[0].text)

        r = ra.get_singleResearchGroupOnID(1)
        self.assertEqual("testgroepdocument",r.desc[0].text)

        r = ResearchGroup(None, "testgroep2", "tg2", 'Mathematics', True, "hiere", "0412864522", list())
        ra.add_researchGroup(r)

        groups=ra.get_researchGroups()
        self.assertEqual(2,len(groups))
        self.assertEqual("testgroep",groups[0].name)
        self.assertEqual("testgroep2", groups[1].name)

        r=ra.get_researchGroupOnName("testgroep")
        self.assertEqual("testgroep", r.name)
        self.assertEqual("tg", r.abbreviation)
        self.assertEqual("Mathematics", r.discipline)
        self.assertEqual(True, r.active)
        self.assertEqual("hier", r.address)
        self.assertEqual("0412864523", r.telNr)
        self.assertEqual(1, len(r.desc))

        r = ra.get_researchGroupOnName("testgroep2")
        self.assertEqual("testgroep2", r.name)
        self.assertEqual("tg2", r.abbreviation)
        self.assertEqual("Mathematics", r.discipline)
        self.assertEqual(True, r.active)
        self.assertEqual("hiere", r.address)
        self.assertEqual("0412864522", r.telNr)
        self.assertEqual(0, len(r.desc))

        ra.remove_researchGroup(1)
        groups = ra.get_researchGroups()
        self.assertEqual(1, len(groups))
        self.assertEqual("testgroep2", groups[0].name)

        r = ResearchGroup(2, "testgroep3", "tg3", 'Mathematics', True, "hiere", "0412864522", list())
        ra.change_researchGroup(r)

        r=ra.get_singleResearchGroupOnID(2)
        self.assertEqual("testgroep3", r.name)
        self.assertEqual("tg3", r.abbreviation)
        self.assertEqual("Mathematics", r.discipline)
        self.assertEqual(True, r.active)
        self.assertEqual("hiere", r.address)
        self.assertEqual("0412864522", r.telNr)
        self.assertEqual(0, len(r.desc))

    def test_EmployeeAccess(self):
        self.setupDB()
        ea = EmployeeAccess()

        ra = ResearchGroupAccess()
        r = ResearchGroup(None, "testgroep", "tg", 'Mathematics', True, "hier", "0412864523", list())
        ra.add_researchGroup(r)

        e=Employee(None,'testpersoon','email@noreply.com',"hier",r.ID,'phd','intern',True,True)
        ea.add_employee(e)

        e=ea.get_employee(1)
        self.assertEqual("testpersoon",e.name)
        self.assertEqual("email@noreply.com", e.email)
        self.assertEqual("hier", e.office)
        self.assertEqual(1, e.research_group)
        self.assertEqual("phd", e.title)
        self.assertEqual("intern", e.internOrExtern)
        self.assertEqual(True, e.active)
        self.assertEqual(True, e.promotor)

        e = Employee(None, 'testpersoon2', 'email2@noreply.com', "hier2", r.ID, 'phd', 'intern', True, True)
        ea.add_employee(e)

        emps=ea.get_employees()
        self.assertEqual(2,len(emps))
        self.assertEqual('testpersoon2', emps[1].name)

        ea.add_employeeRole(1,'admin')
        emps=ea.get_admins()
        self.assertEqual(1,len(emps))
        self.assertEqual('testpersoon',emps[0].name)

        e=ea.get_employeeOnName('testpersoon')
        self.assertEqual("email@noreply.com", e.email)
        self.assertEqual("hier", e.office)
        self.assertEqual(1, e.research_group)
        self.assertEqual("phd", e.title)
        self.assertEqual("intern", e.internOrExtern)
        self.assertEqual(True, e.active)
        self.assertEqual(True, e.promotor)

        ea.remove_employee(1)
        emps = ea.get_employees()
        self.assertEqual(1, len(emps))
        self.assertEqual('testpersoon2', emps[0].name)

        ea.add_employeeRole(2,'admin')
        ea.add_employeeRole(2, 'staff')

        rol=ea.get_employeeRoles(2)
        self.assertEqual(2,len(rol))
        self.assertEqual('admin', rol[0])

        e = Employee(2, 'testpersoon3', 'email3@noreply.com', "hier2", r, 'phd', 'intern', True, True)
        ea.change_employee(e)

        e = ea.get_employee(2)
        self.assertEqual("testpersoon3", e.name)
        self.assertEqual("email3@noreply.com", e.email)
        self.assertEqual("hier2", e.office)
        self.assertEqual(1, e.research_group)
        self.assertEqual("phd", e.title)
        self.assertEqual("intern", e.internOrExtern)
        self.assertEqual(True, e.active)
        self.assertEqual(True, e.promotor)

    def test_ProjectAccess(self):
        self.setupDB()
        pa=ProjectAccess()
        ea = EmployeeAccess()

        p=Project(None,"testproject",3,True)
        pa.add_project(p)
        p=pa.get_project(1)
        self.assertEqual("testproject", p.title)
        self.assertEqual(3, p.maxStudents)

        p = Project(None, "testproject2", 4, True)
        pa.add_project(p)
        projs=pa.get_projects()
        self.assertEqual(2,len(projs))
        self.assertEqual("testproject2",projs[1].title)

        ra = ResearchGroupAccess()
        r = ResearchGroup(None, "testgroep", "tg", 'Mathematics', True, "hier", "0412864523", list())
        ra.add_researchGroup(r)

        pa.add_projectResearchgroup(1,1)
        p = pa.get_project(1)
        self.assertEqual(1,p.researchGroup[0])

        rp=pa.get_projectresearchgroups(1)
        self.assertEqual(1, rp[0])

        pa.add_projectRelation(1,2)
        p = pa.get_project(1)
        self.assertEqual(2,p.relatedProject[0])

        rpj=pa.get_projectRelations(1)
        self.assertEqual(2, rpj[0])

        pa.add_projectTag(1,'tag')
        p = pa.get_project(1)
        self.assertEqual('tag', p.tag[0])

        tags=pa.get_projectTags(1)
        self.assertEqual('tag', tags[0])

        e = Employee(None, 'testpersoon', 'email@noreply.com', "hier", r.ID, 'phd', 'intern', True, True)
        ea.add_employee(e)
        pa.add_projectPromotor(1,1)
        p = pa.get_project(1)
        self.assertEqual(1, p.promotor[0])

        prom=pa.get_projectPromotors(1)
        self.assertEqual(1,prom[0])

        pa.add_projectTypeConnection(1,'Master thesis')
        p = pa.get_project(1)
        self.assertEqual('Master thesis', p.type[0])

        types=pa.get_typesFromProject(1)
        self.assertEqual('Master thesis', types[0])

        pa.add_projectYears(1,2019)
        p = pa.get_project(1)
        self.assertEqual(2019, p.activeYear[0])

        doc=Document(None, 'dutch', 'testDocument')
        pa.add_projectDocument(1,doc)
        p = pa.get_project(1)
        self.assertEqual('testDocument', p.desc[0].text)

    def test_StudentAccess(self):
        self.setupDB()
        sa=StudentAccess()

        stu=Student(None,"joske",'20170000')
        sa.add_student(stu)

        stu=sa.get_student(1)
        self.assertEqual('joske',stu.name)
        self.assertEqual(20170000,stu.studentNumber)

        sa.add_student(Student(None,'jefke','20170001'))

        stus=sa.get_students()
        self.assertEqual(2,len(stus))
        self.assertEqual('jefke',stus[1].name)
        self.assertEqual(20170001, stus[1].studentNumber)





if __name__ == '__main__':
    unittest.main()