from flask.ext.login import UserMixin, AnonymousUser

class User(UserMixin):
    
    def __init__(self, id, username, password, name=None, city=None):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.city = city
        self.role = 1

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.role == 0:
            return False
        else:
            return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Anonymous(AnonymousUser):
    name = u"Anonymous"
