from api.util.config import db
from sqlalchemy import text

class ToolReports(db.Model):
    __tablename__ = 'toolreports'
    tool_id = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(20), nullable=False)
    user_id =  db.Column(db.Integer, nullable=False)
    report_id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.DateTime)

    def __init__(self, **args):
        self.tool_id = args.get('tool_id ')
        self.status = args.get('status')
        self.comment = args.get('comment')
        self.user_id = args.get('user_id')
        self.report_id = args.get('report_id')
        self.report_date = args.get('report_date')

    @property
    def pk(self):
        return self.report_id

    @staticmethod
    def getAllToolReports():
        return ToolReports().query.all()

    @staticmethod
    def getToolReports(tool_id):
        sql = text("select tr.status,tr.comment,CONCAT(u.first_name,' ',u.last_name) as user_name, \
        tr.report_date from public.toolreports tr \
        left join public.users u \
        on u.user_id = tr.user_id \
        where tr.tool_id = :tool_id \
        order by report_id desc")
        return db.engine.execute(sql,{'tool_id':tool_id})

    @staticmethod
    def createToolReport(report):
        sql = text("insert into public.toolreports \
            (tool_id,status,comment,user_id) \
            VALUES(:tool_id, :status, :comment, :user_id)")
        try: 
            db.engine.execute(sql,{'tool_id':report['tool_id'],
            'status': report['status'],
            'comment': report['comment'],
            'user_id': report['user_id']
            })
            return 'Successfully Created New Tool Report'
        except:
            return 'Error Creating New Tool Report'

    @staticmethod
    def getLatestReport(tool_id):
        sql = text("select tr.status,tr.comment,CONCAT(u.first_name,' ',u.last_name) as user_name, \
        tr.report_date, tr.report_id \
         from public.toolreports tr \
        left join public.users u \
        on u.user_id = tr.user_id \
        where tr.tool_id = :tool_id \
        order by report_id desc \
        LIMIT 1")
        return db.engine.execute(sql,{'tool_id':tool_id})
    @staticmethod
    def updateToolReport(toolReport):
        sql = text("UPDATE public.toolreports \
            SET \
            tool_id = :tool_id \
            ,status = :status \
            ,comment = :comment \
            ,user_id = :user_id \
            ,report_date = :report_date \
            WHERE report_id = report_id")
        try:
            db.engine.execute(sql,
            {'tool_id' : toolReport['tool_id'],
            'status' : toolReport['status'],
            'comment' : toolReport['comment'],
            'user_id' : toolReport['user_id'],
            'report_date' : toolReport['report_date'],
            })
            return 'Successfully Edited Tool Report'
        except:
            return 'Error Editing Tool Report'
 
    @staticmethod
    def deleteToolReport(report_id):
        sql = text("delete from public.toolreports where report_id = :id ")
        try: 
            db.engine.execute(sql,{'id':report_id})
            return 'Successfully Deleted Tool Report'
        except:
            return 'Error Deleting Tool Report'
