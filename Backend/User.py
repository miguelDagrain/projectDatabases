from flask_login import LoginManager
class User:
    def __init__(self,session):
        self.session=session
        self.auth=False
        self.active=True
        self.anon=False

    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.session.sessionId)

    def is_authenticated(self):

        return self.auth

    def is_anonymous(self):
        return self.anon
