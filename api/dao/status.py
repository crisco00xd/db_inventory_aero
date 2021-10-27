from api.util.config import db


class Status(db.Model):
    __tablename__ = 'status'
    status_id = db.Column(db.Integer, primary_key=True)
    stat = db.Column(db.String(16), nullable=False)

    request = db.relationship("Requests")

    def __init__(self, **args):
        self.stat = args.get('stat')

    @property
    def pk(self):
        return self.status_id

    @staticmethod
    def getStatuses():
        return Status().query.all()

    @staticmethod
    def getStatusById(stat_id):
        return Status().query.filter_by(status_id=stat_id).first()