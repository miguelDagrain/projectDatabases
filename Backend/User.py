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