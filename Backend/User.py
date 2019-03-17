from flask_login import UserMixin
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

    def login(self,userName,password):
        if(userName=='admin' and password=="hunter1"):
            self.session.studentId=1
            self.auth=True
            self.roles=('admin','user')
            self.active = True
            self.anon = False
            return True
        elif(userName=='user' and password=='hunter2'):
            self.session.studentId = 2
            self.auth=True
            self.roles=('user')
            self.active = True
            self.anon = False
            return True
        else:
            self.auth = False
            self.roles=None
            self.active = False
            self.anon = False
            return False
        # ldap_server = "192.168.0.175"
        # username = "user"
        # password = "pass"
        # # the following is the user_dn format provided by the ldap server
        # user_dn = "uid=" + username + ",ou=someou,dc=somedc,dc=local"
        # # adjust this to your base dn for searching
        # base_dn = "dc=somedc,dc=local"
        # connect = ldap.initialize(ldap_server)
        # connect.set_option(ldap.OPT_REFERRALS, 0)
        # connect.simple_bind_s('Manager', 'secret')
        # result = connect.search_s('cn=Manager,dc=maxcrc,dc=com',
        #                           ldap.SCOPE_SUBTREE,
        #                           'userPrincipalName=user@somedomain.com',
        #                           ['memberOf'])
        # search_filter = "uid=" + username
        # try:
        #     # if authentication successful, get the full user data
        #     connect.bind_s(user_dn, password)
        #     result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        #     # return all user data results
        #     connect.unbind_s()
        #     print(result)
        #     login_user(User(Session(1, 1, 0, 0)))
        #     flash('Logged in successfully.')
        #
        #     flash("you are now logged in")
        # except:
        #     connect.unbind_s()
        #     print("authentication error")
