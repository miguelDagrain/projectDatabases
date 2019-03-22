from flask_login import UserMixin
import ldap
from DataAccess import EmployeeAccess

class User(UserMixin):
    def __init__(self,session):
        self.session=session
        self.auth=False
        self.active=True
        self.anon=False
        self.roles=list

    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.session.studentId)

    def is_authenticated(self):

        return self.auth

    def is_anonymous(self):
        return self.anon

    def is_admin(self):
        return 'admin' in self.roles

    def get_roles(self):
        return self.roles

    def login(self,userName,password,conn):
        # if(userName=='admin' and password=="hunter1"):
        #     self.session.studentId=1
        #     self.auth=True
        #     self.roles=('admin','user')
        #     self.active = True
        #     self.anon = False
        #     return True
        # elif(userName=='user' and password=='hunter2'):
        #     self.session.studentId = 2
        #     self.auth=True
        #     self.roles=('user')
        #     self.active = True
        #     self.anon = False
        #     return True
        # else:
        #     self.auth = False
        #     self.roles=None
        #     self.active = False
        #     self.anon = False
        #     return False
        ldap_server = 'ldap:///ldap.pdbldap.com/'
        ldap_conn = ldap.initialize(ldap_server)
        user_dn = "uid=" + userName + ",ou=People,dc=pdbldap,dc=com"
        base_dn = "dc=pdbldap,dc=com"
        search_filter = "uid=" + userName
        try:
            ldap_conn.bind_s(user_dn,password)
            result = ldap_conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
            ldap_conn.unbind_s()
            employeeid= int(result[0][1]['uidNumber'][0])
            eacces=EmployeeAccess(conn)
            self.session.studentId = employeeid
            self.auth=True
            self.roles=eacces.get_employeeRoles(employeeid)
            self.active = True
            self.anon = False
            return True
        except:
            self.auth = False
            self.roles=None
            self.active = False
            self.anon = False
            ldap_conn.unbind_s()
            # print("authentication error")
            return False