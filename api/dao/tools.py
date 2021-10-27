from api.util.config import db
from sqlalchemy import text

class Tools(db.Model):
    __tablename__ = 'tools'
    name = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20))
    image = db.Column(db.String(50))
    id = db.Column(db.String(20), primary_key = True)

    def __init__(self, **args):
        self.id = args.get('id')
        self.name = args.get('name')
        self.category = args.get('category')
        self.image = args.get('image')

    @property
    def pk(self):
        return self.id
    #table data (OLD)
    @staticmethod
    def getTools():
        sql = text("select t.id,t.name,t.category, t.image \
        from public.tools t")
        return db.engine.execute(sql)

    @staticmethod
    def getAllTools():
        sql = text("select * \
        from public.tools t")
        return db.engine.execute(sql)

    #view tool
    @staticmethod
    def getToolById(tid):
        sql = text("select t.id,t.name,t.category,t.image,tr.status,tr.comment,tr.user_id,  \
            CONCAT(u.first_name,' ',u.last_name) as user_name, tr.report_id,tr.report_date \
            from ( \
            select tool_id,max(report_id) as report_id from public.toolreports group by tool_id) as latest_report \
            inner join public.toolreports tr  \
            on tr.report_id = latest_report.report_id \
            right join public.tools t \
            on t.id = tr.tool_id \
            left join public.users u \
            on tr.user_id = u.user_id \
            where t.id = :tool_id")
        return db.engine.execute(sql,{'tool_id':tid})

    #create tool
    @staticmethod
    def createTool(tool):
        sql = text("insert into public.tools\
            (id,name,category,image) \
            VALUES( :id, :name, :category, :image)")
        try: 
            db.engine.execute(sql,
            {'id':tool['id'],
            'name':tool['name'],
            'category':tool['category'],
            'image': tool['comment']
            })
            return 'Successfully Created New Tool'
        except:
            return 'Error Creating New Tool'

    #update tool
    @staticmethod
    def updateTool(tool):
        sql = text("update public.tools set \
                name = :name, \
                category = :category , \
                image = :image , \
                where id = :id ")
        try: 
            db.engine.execute(sql,
            {'id':tool['id'],
            'name':tool['name'],
            'category':tool['category'],
            'image': tool['comment']
            })
            return 'Successfully Edited Tool'
        except:
            return 'Error Editing Tool'

    #delete tool
    @staticmethod
    def deleteTool(tool_id):
        sql = text("delete from public.tools where id = :id ")
        try: 
            db.engine.execute(sql,{'id':tool_id})
            return 'Successfully Deleted Tool'
        except:
            return 'Error Deleting Tool'
    #New Table Data Query
    @staticmethod
    def getToolTable():
        sql = text("select t.id,t.name,t.category,t.image,tr.status,tr.comment,tr.user_id,  \
            CONCAT(u.first_name,' ',u.last_name) as user_name, tr.report_id,tr.report_date \
            from ( \
            select tool_id,max(report_id) as report_id from public.toolreports group by tool_id) as latest_report \
            inner join public.toolreports tr  \
            on tr.report_id = latest_report.report_id \
            right join public.tools t \
            on t.id = tr.tool_id \
            left join public.users u \
            on tr.user_id = u.user_id ")
        return db.engine.execute(sql)

    @staticmethod
    def getToolsFromUser(user_id):
        sql = text("select t.id, t.name, t.category, t.image  \
        from (select tool_id, max(report_id) as report_id \
        from public.toolreports group by tool_id) as latest_report \
        inner join public.toolreports tr on tr.report_id = latest_report.report_id \
        right join public.tools t on t.id = tr.tool_id where tr.user_id = :user_id \
        and tr.status != 'in storage'")
        return db.engine.execute(sql, {'user_id':user_id})
     