from api.util.config import db


class Parts(db.Model):
    __tablename__ = 'parts'
    part_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.dept_id'), nullable=False)
    is_electronic = db.Column(db.Boolean, nullable=False)
    is_software = db.Column(db.Boolean, nullable=False)

    request = db.relationship("Requests")

    def __init__(self, **args):
        self.name = args.get('name')
        self.stock = args.get('stock')
        self.dept_id = args.get('dept_id')
        self.is_electronic = args.get('is_electronic')
        self.is_software = args.get('is_software')

    @property
    def pk(self):
        return self.part_id

    @staticmethod
    def getParts():
        return Parts().query.all()

    @staticmethod
    def getPartById(pid):
        return Parts().query.filter_by(part_id=pid).first()

    @staticmethod
    def getPartByName(pname):
        return Parts().query.filter_by(name=pname).first()

    @staticmethod
    def getPartsByDepartment(did):
        return Parts().query.filter_by(dept_id=did).all()

    @staticmethod
    def getElectronicPartsByDepartment(did):
        return Parts().query.filter_by(dept_id=did, is_electronic=True).all()

    @staticmethod
    def getSoftwarePartsByDepartment(did):
        return Parts().query.filter_by(dept_id=did, is_software=True).all()

    @staticmethod
    def getNormalPartsByDepartment(did):
        return Parts().query.filter_by(dept_id=did, is_software=False, is_electronic=False).all()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def delete(pid):
        part = Parts.getPartById(pid)
        if not part:
            return None
        db.session.delete(part)
        db.session.commit()
        return part

    @staticmethod
    def updateStock(pid, stock):
        part = Parts.getPartById(pid)
        part.stock = stock
        db.session.commit()
        return part

    @staticmethod
    def updatePart(pid, **args):
        part = Parts.getPartById(pid)
        part.name = args.get('name')
        part.stock = args.get('stock')
        part.dept_id = args.get('dept_id')
        part.is_electronic = args.get('is_electronic')
        part.is_software = args.get('is_software')
        db.session.commit()
        return part

