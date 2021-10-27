from api.util.config import db
import datetime
from api.dao.parts import Parts


class Requests(db.Model):
    __tablename__ = 'requests'
    request_id = db.Column(db.Integer, primary_key=True)
    date_requested = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc).astimezone)
    quantity = db.Column(db.Integer, nullable=False)
    date_fulfilled = db.Column(db.DateTime, nullable=True)
    amount_used = db.Column(db.Integer, nullable=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    fulfiller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.part_id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), default=1) #Pending=1

    def __init__(self, **args):
        self.date_requested = args.get('date_requested')
        self.quantity = args.get('quantity')
        self.date_fulfilled = args.get('date_fulfilled')
        self.amount_used = args.get('amount_used')
        self.requester_id = args.get('requester_id')
        self.fulfiller_id = args.get('fulfiller_id')
        self.part_id = args.get('part_id')
        self.status_id = args.get('status_id')

    @property
    def pk(self):
        return self.request_id

    @staticmethod
    def getRequests():
        return Requests().query.all()

    @staticmethod
    def getRequestById(rid):
        return Requests().query.filter_by(request_id=rid).first()


    @staticmethod
    def getUnfulfilledRequests():
        # Pending = 1
        return Requests().query.filter_by(status_id=1).all()

    @staticmethod
    def getAllRequestsByDepartment(did):
        return Requests().query.join(Parts).filter_by(dept_id=did).all()

    @staticmethod
    def getUnfulfilledRequestsByDepartment(did):
        return Requests().query.filter_by(status_id=1).join(Parts).filter_by(dept_id=did).all()

    @staticmethod
    def getRequestsHistoryByDepartment(did):
        return Requests().query.filter(Requests.status_id != 1).join(Parts).filter_by(dept_id=did).all()

    @staticmethod
    def getRequestsByUser(uid):
        return Requests().query.filter_by(requester_id=uid).all()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def updateRequest(rid, **args):
        request = Requests.getRequestById(rid)
        request.quantity = args.get('quantity')
        db.session.commit()
        return request

    @staticmethod
    def cancelRequest(rid):
        request = Requests.getRequestById(rid)
        request.status_id = 3
        db.session.commit()
        return request

    @staticmethod
    def deleteRequest(rid):
        request = Requests.getRequestById(rid)
        db.session.delete(request)
        db.session.commit()
        return request

    @staticmethod
    def updateStatus(rid, **args):
        request = Requests.getRequestById(rid)
        request.fulfiller_id = args.get('fulfiller_id')
        request.status_id = args.get('status_id')
        request.date_fulfilled = datetime.datetime.now(datetime.timezone.utc).astimezone()
        if args.get('status_id') == 2:
            part = Parts.getPartById(request.part_id)
            part.stock = part.stock - request.quantity
        db.session.commit()
        return request

    @staticmethod
    def addAmountUsed(rid, used):
        request = Requests.getRequestById(rid)
        request.amount_used = used
        #request.status_id = 5      //temporary commented
        part = Parts.getPartById(request.part_id)
        part.stock = part.stock + request.quantity - used
        db.session.commit()
        return request
