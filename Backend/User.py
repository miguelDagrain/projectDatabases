from flask_login import UserMixin
# import ldap
from DataAccess import employeeAccess
from DataAccess import studentAccess
from config import config_data
from ldapConfig import ldapConfig_data
from Session import EORS
import ldapConfig


class User(UserMixin):
    def __init__(self, session):
        self.session = session
        self.auth = False
        self.active = True
        self.anon = False
        self.roles = list()

    def is_active(self):
        return self.active

    """"
    returns a letter denoting whether it is a employee or student and the ID
    """

    def get_id(self):
        if self.session is not None:
            if self.session.EORS == EORS.EMPLOYEE:
                return str("E" + str(self.session.ID))
            elif self.session.EORS == EORS.STUDENT:
                return str("S" + str(self.session.sessionID))
            else:
                return str("U" + str(self.session.ID))

    def is_authenticated(self):

        return self.auth

    def is_anonymous(self):
        return self.anon

    def is_admin(self):
        return 'admin' in self.roles

    def get_roles(self):
        return self.roles

    def login(self, userName, password):
        if config_data['loginMode'] == 'normal':
            return self.normalLogin(userName, password)
        elif config_data['loginMode'] == 'ldap':
            return self.ldapLogin(userName, password)
        else:
            print("unknown login type: " + config_data['login'])
            return False

    def ldapLogin(self, userName, password):
        ldap_server = ldapConfig_data['serverAddress']
        ldap_conn = ldap.initialize(ldap_server)
        user_dn = "cn=" + userName + ",ou=" + ldapConfig_data["ou"] + ",dc=" + ldapConfig_data["dcName"] + ",dc=" + \
                  ldapConfig_data['dcDomain']
        base_dn = "dc=" + ldapConfig_data["dcName"] + ",dc=" + ldapConfig_data['dcDomain']
        search_filter = "uid=" + userName
        try:
            from DataAccess.employeeAccess import EmployeeAccess
            from DataAccess.studentAccess import StudentAccess
            ldap_conn.bind_s(user_dn, password)
            ldap_conn.unbind_s()
            eacces = EmployeeAccess()

            emp = eacces.get_employeeOnName(userName)
            if emp is not None:
                self.session.ID = emp.id
                self.session.EORS = EORS.EMPLOYEE
                self.auth = True
                self.roles = eacces.get_employeeRoles(emp.id)
                self.roles.append("employee")
                self.roles.append("user")
                self.active = True
                self.anon = False
                return True
            sacces = StudentAccess()
            number = userName[1:]
            number = "2" + number
            stu = sacces.get_studentOnStudentNumber(number)
            if stu is not None:
                self.session.ID = stu.studentID
                self.session.EORS = EORS.STUDENT
                self.auth = True
                self.roles = list()
                self.roles.append("student")
                self.roles.append("user")
                self.active = True
                self.anon = False
                return True

            self.auth = False
            self.roles = None
            self.active = False
            self.anon = False
            return False

        except:
            self.auth = False
            self.roles = None
            self.active = False
            self.anon = False
            ldap_conn.unbind_s()
            # print("authentication error")
        return False

    def normalLogin(self, userName, password):
        if userName == 'admin' and password == "hunter1":
            self.session.ID = 16
            self.session.EORS = EORS.EMPLOYEE
            self.auth = True
            self.roles = ('employee', 'admin', 'user')
            self.active = True
            self.anon = False
            return True
        elif userName == 'employee' and password == 'hunter2':
            self.session.ID = 2
            self.session.EORS = EORS.EMPLOYEE
            self.auth = True
            self.roles = ('employee', 'user')

            self.active = True
            self.anon = False
            return True
        elif userName == 'student' and password == 'hunter3':
            self.session.ID = 1
            self.session.EORS = EORS.STUDENT
            self.auth = True
            self.roles = ('student', 'user')
            self.active = True
            self.anon = False
            return True
        else:
            self.auth = False
            self.roles = None
            self.active = False
            self.anon = False
            return False
