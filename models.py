from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Creates a User"""

    __tablename__ = 'users'

    username = db.Column(db.VARCHAR(20),
                         primary_key=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.VARCHAR(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.VARCHAR(30),
                           nullable=False)
    last_name = db.Column(db.VARCHAR(30),
                           nullable=False)
    
    @classmethod
    def hash_password(self, password):
        hash = bcrypt.generate_password_hash(password)
        return hash.decode('utf8')
    
    @classmethod
    def authenticate(self, username, password):
        u = User.query.get_or_404(username)
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False
        
class Feedback(db.Model):
    """Creates feedback"""

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.VARCHAR(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.Text,
                         db.ForeignKey('users.username', ondelete='CASCADE'),
                         nullable=False)
    
    user = db.relationship('User', backref='feedbacks')