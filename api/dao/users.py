from api.util.config import db
from sqlalchemy import text

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    is_leader = db.Column(db.Boolean, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.dept_id'), nullable=False)

    request = db.relationship("Requests", foreign_keys='Requests.requester_id')
    fulfilled_request = db.relationship("Requests", foreign_keys='Requests.fulfiller_id')

    def __init__(self, **args):
        self.first_name = args.get('first_name')
        self.last_name = args.get('last_name')
        self.email = args.get('email')
        self.password = args.get('password')
        self.is_leader = args.get('is_leader')
        self.dept_id = args.get('dept_id')

    @property
    def pk(self):
        return self.user_id

    @staticmethod
    def getUsers():
        return Users().query.all()

    @staticmethod
    def getUserById(uid):
        return Users().query.filter_by(user_id=uid).first()

    @staticmethod
    def getUserByEmail(uemail):
        return Users().query.filter_by(email=uemail).first()

    @staticmethod
    def getLeaders():
        return Users().query.filter_by(is_leader=True).all()

    @staticmethod
    def getNonLeaders():
        return Users().query.filter_by(is_leader=False).all()

    #create user
    @staticmethod
    def createUser(user):
        sql = text("insert into public.users\
            (first_name,last_name,email,password,is_leader,dept_id) \
            VALUES(:first_name,:last_name,:email,:password,:is_leader,:dept_id)")
        try: 
            db.engine.execute(sql,
            {'first_name':user['first_name'],
            'last_name':user['last_name'],
            'email':user['email'],
            'password': user['password'],
            'is_leader': user['is_leader'],
            'dept_id': user['dept_id']
            })
            return 'Successfully Created New User'
        except:
            return 'Error Creating New User'

    #update user
    @staticmethod
    def updateUser(user):
        sql = text("UPDATE public.users\
            SET \
            first_name = :first_name \
            ,last_name = :last_name \
            ,email = :email \
            ,password = :password \
            ,is_leader = :is_leader \
            ,dept_id = :dept_id \
            WHERE user_id = :user_id")
        try: 
            db.engine.execute(sql,
            {'first_name':user['first_name'],
            'last_name':user['last_name'],
            'email':user['email'],
            'password': user['password'],
            'is_leader': user['is_leader'],
            'dept_id': user['dept_id'],
            'user_id': user['user_id']
            })
            return 'Successfully Edited User'
        except:
            return 'Error Editing User'

    #delete user
    @staticmethod
    def deleteUser(user_id):
        sql = text("delete from public.users where user_id = :user_id")
        try: 
            db.engine.execute(sql,{'user_id':user_id})
            return 'Successfully Deleted User'
        except:
            return 'Error Deleting User'
 
 