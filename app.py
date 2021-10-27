from flask import request
from api.util.config import app
from api.handler.departments import DepartmentsHandler
from api.handler.parts import PartsHandler
from api.handler.requests import RequestsHandler
from api.handler.status import StatusHandler
from api.handler.users import UsersHandler
from api.handler.tools import ToolsHandler
from api.handler.toolreports import ToolReportsHandler


@app.route('/', methods=['GET'])
def home():
    return "Hi"


@app.route('/departments', methods=['GET'])
def getAllDepartments():
    return DepartmentsHandler.getAllDepartments()


@app.route('/parts', methods=['GET', 'POST'])
def getAllPartsOrCreate():
    if request.method == 'GET':
        return PartsHandler.getAllParts()
    else:
        return PartsHandler.createOrUpdatePart(request.json)


@app.route('/departments/<int:did>', methods=['GET'])
def getDepartmentById(did):
    return DepartmentsHandler.getDepartmentById(did)


@app.route('/parts/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def getPartByIdOrUpdate(pid):
    if request.method == 'GET':
        return PartsHandler.getPartById(pid)
    elif request.method == 'DELETE':
        return PartsHandler.deletePart(pid)
    else:
        if len(request.json) == 1:
            return PartsHandler.updateStock(pid, request.json)
        else:
            return PartsHandler.updatePart(pid, request.json)


@app.route('/parts/dept/<int:did>', methods=['GET'])
def getPartsByDeptId(did):
    return PartsHandler.getPartsByDepartment(did)


@app.route('/parts/normal/dept/<int:did>', methods=['GET'])
def getNormalPartsByDeptId(did):
    return PartsHandler.getNormalPartsByDepartment(did)


@app.route('/parts/electronic/dept/<int:did>', methods=['GET'])
def getElectronicPartsByDeptId(did):
    return PartsHandler.getElectronicPartsByDepartment(did)


@app.route('/parts/software/dept/<int:did>', methods=['GET'])
def getSoftwarePartsByDeptId(did):
    return PartsHandler.getSoftwarePartsByDepartment(did)


@app.route('/requests', methods=['GET', 'POST'])
def getAllRequestsOrCreate():
    if request.method == 'GET':
        return RequestsHandler.getAllRequests()
    else:
        return RequestsHandler.createRequest(request.json)


@app.route('/requests/<int:rid>', methods=['GET', 'PUT', 'DELETE'])
def getRequestByIdOrEdit(rid):
    if request.method == 'GET':
        return RequestsHandler.getRequestById(rid)
    elif request.method == 'DELETE':
        return RequestsHandler.cancelRequest(rid)
    else:
        if 'fulfiller_id' not in request.json:
            if 'amount_used' in request.json:
                return RequestsHandler.addAmountUsed(rid, request.json)
            else:
                return RequestsHandler.updateRequest(rid, request.json)
        else:
            return RequestsHandler.updateStatus(rid, request.json)


@app.route('/requests/delete/<int:rid>', methods=['DELETE'])
def deleteRequest(rid):
    return RequestsHandler.deleteRequest(rid)


@app.route('/requests/user/<int:uid>', methods=['GET'])
def getRequestsByUser(uid):
    return RequestsHandler.getRequestsByUser(uid)


@app.route('/requests/dept/<int:dept_id>', methods=['GET'])
def getAllRequestsByDept(dept_id):
    return RequestsHandler.getAllRequestsByDepartment(dept_id)


@app.route('/requests/pending/dept/<int:dept_id>', methods=['GET'])
def getUnfulfilledRequestsByDept(dept_id):
    return RequestsHandler.getUnfulfilledRequestsByDepartment(dept_id)


@app.route('/requests/history/dept/<int:dept_id>', methods=['GET'])
def getRequestsHistoryByDepartment(dept_id):
    return RequestsHandler.getRequestsHistoryByDepartment(dept_id)


@app.route('/statuses', methods=['GET'])
def getAllStatuses():
    return StatusHandler.getAllStatuses()


@app.route('/users', methods=['GET'])
def getAllUsers():
    return UsersHandler.getAllUsers()


@app.route('/user/<int:uid>', methods=['GET'])
def getUserById(uid):
    return UsersHandler.getUserById(uid)


@app.route('/leaders', methods=['GET'])
def getLeaders():
    return UsersHandler.getLeaders()


@app.route('/nonleaders', methods=['GET'])
def getNonLeaders():
    return UsersHandler.getNonLeaders()


@app.route('/login', methods=['POST'])
def login():
    return UsersHandler.login(request.json)


@app.route('/logout', methods=['GET'])
def logout():
    return UsersHandler.logout()
    
@app.route('/get-all-tools',methods=['GET'])
def getAllTools():
    return ToolsHandler.getAllTools()

@app.route('/get-tools',methods=['GET'])
def getTools():
    return ToolsHandler.getTools()

@app.route('/get-tools-from-user/<int:uid>',methods=['GET'])
def getToolsFromUser(uid):
    return ToolsHandler.getToolsFromUser()

@app.route('/get-tool/<string:tool_id>',methods=['GET'])
def getToolById(tool_id):
    return ToolsHandler.getToolById(tool_id)

@app.route('/tool',methods=['POST','PUT','DELETE'])
def manageTool():
    if request.method == 'POST':
        return ToolsHandler.createTool(request.json)
    if request.method == 'PUT':
        return ToolsHandler.updateTool(request.json)
    if request.method == 'DELETE':
        return ToolsHandler.deleteTool(request.json)
    else:
        return 'BAD REQUEST'

@app.route('/delete-tool/<string:tool_id>',methods=['DELETE'])
def deleteTool(tool_id):
    return ToolsHandler.deleteTool(tool_id)


@app.route('/get-tool-reports',methods=['GET'])
def getAllToolReports():
    return ToolReportsHandler.getAllToolReports()

@app.route('/get-tool-reports/<string:tool_id>',methods=['GET'])
def getToolReports(tool_id):
    return ToolReportsHandler.getToolReports(tool_id)

@app.route('/delete-tool-report/<string:report_id>',methods=['DELETE'])
def deleteToolReport(report_id):
    return ToolReportsHandler.deleteToolReport(report_id)

@app.route('/create-tool-report',methods=['POST'])
def createToolReport():
    return ToolReportsHandler.createToolReport(request.json)

@app.route('/get-latest-report/<string:tool_id>',methods=['GET'])
def getLatestReport(tool_id):
    return ToolReportsHandler.getLatestReport(tool_id)

@app.route('/update-tool-report',methods=['PUT'])
def updateToolReport():
    return ToolReportsHandler.updateToolReport(request.json)

@app.route('/create-user',methods=['POST'])
def createUser():
    return UsersHandler.createUser(request.json)

@app.route('/update-user',methods=['PUT'])
def updateUser():
    return UsersHandler.createUser(request.json)

@app.route('/delete-user/<string:user_id>',methods=['DELETE'])
def deleteUser(user_id):
    return UsersHandler.deleteUser(user_id)
    
@app.route('/tool-table',methods=['GET'])
def getToolTable():
    return ToolsHandler.getToolTable()

if __name__ == '__main__':
    app.run()
