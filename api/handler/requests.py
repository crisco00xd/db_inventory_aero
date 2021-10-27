from flask import jsonify
from flask_mail import Message
from api.dao.requests import Requests
from api.handler.parts import PartsHandler
from api.handler.status import StatusHandler
from api.util.config import mail
from api.util.utilities import Utilities
from api.handler.users import UsersHandler
from api.dao.parts import Parts

class RequestsHandler:

    @staticmethod
    def getAllRequests():
        try:
            requests = Requests.getRequests()
            result_list = []
            for request in requests:
                result_list.append(Utilities.to_dict(request))
            result = {
                "message": "Success!",
                "requests": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getRequestById(rid):
        try:
            request = Requests.getRequestById(rid)
            request_dict = Utilities.to_dict(request)
            result = {
                "message": "Success!",
                "request": request_dict
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getRequestDictById(rid):
        try:
            request = Requests.getRequestById(rid)
            request_dict = Utilities.to_dict(request)
            return request_dict
        except Exception as e:
            return None

    @staticmethod
    def getUnfulfilledRequests():
        try:
            requests = Requests.getUnfulfilledRequests()
            result_list = []
            for request in requests:
                result_list.append(Utilities.to_dict(request))
            result = {
                "message": "Success!",
                "requests": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getAllRequestsByDepartment(did):
        try:
            requests = Requests.getAllRequestsByDepartment(did)
            result_list = []
            for request in requests:
                result_list.append(Utilities.to_dict(request))
            result = {
                "message": "Success!",
                "requests": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getUnfulfilledRequestsByDepartment(did):
        try:
            requests = Requests.getUnfulfilledRequestsByDepartment(did)
            result_list = []
            for request in requests:
                result_list.append(Utilities.to_dict(request))
            result = {
                "message": "Success!",
                "requests": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getRequestsHistoryByDepartment(did):
        try:
            requests = Requests.getRequestsHistoryByDepartment(did)
            result_list = []
            for request in requests:
                result_list.append(Utilities.to_dict(request))
            result = {
                "message": "Success!",
                "requests": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getRequestsByUser(uid):
        try:
            requests = Requests.getRequestsByUser(uid)
            result_list = []
            for request in requests:
                result_list.append(Utilities.to_dict(request))
            result = {
                "message": "Success!",
                "requests": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def createRequest(json):
        valid_parameters = Utilities.verify_parameters(json, ['quantity', 'requester_id', 'part_id'])
        if valid_parameters:   
            try:
                # availableQuantity = PartsHandler.getPartById(json['part_id'])[0]['part']['stock']
                availableQuantity = Parts.getPartById(json['part_id']).stock
                if(availableQuantity < json['quantity']):
                    return jsonify(reason="Not enough stock"), 401
                else:
                    newRequest = Requests(**valid_parameters).create()
                    result = {
                        "message": "Success!",
                        "request": Utilities.to_dict(newRequest)
                    }
                    RequestsHandler.__sendRequestMail(json)
                    return jsonify(result), 200
            except Exception as e:
                return jsonify(reason="Server error", error=e.__str__()), 500
        else:
            return jsonify(reason="Invalid parameters"), 400

    @staticmethod
    def __sendRequestMail(request):
        requester = UsersHandler.getUserDictById(request['requester_id'])
        part = PartsHandler.getPartDictById(request['part_id'])
        recipients = UsersHandler.getLeaderEmails()

        subject = "RUMAir Inventory: Part Requested"
        message = Message(
            subject, recipients=recipients
        )
        message.body = f"{requester['first_name']} {requester['last_name']} wants to take out {request['quantity']} {part['name']}(s). There currently is {part['stock']} in stock. Please go to app to manage this request."

        mail.send(message)

    @staticmethod
    def updateRequest(rid, json):
        valid_parameters = Utilities.verify_parameters(json, ['quantity'])
        if valid_parameters:
            try:
                updatedRequest = Requests.updateRequest(rid, **valid_parameters)
                result = {
                    "message": "Success!",
                    "part": Utilities.to_dict(updatedRequest)
                }
                return jsonify(result), 200
            except Exception as e:
                return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def cancelRequest(rid):
        updatedRequest = Requests.cancelRequest(rid)
        result = {
            "message": "Success!",
            "part": Utilities.to_dict(updatedRequest)
        }
        return jsonify(result), 200

    @staticmethod
    def deleteRequest(rid):
        deletedRequest = Requests.deleteRequest(rid)
        result = {
            "message": "Success!",
            "request": Utilities.to_dict(deletedRequest)
        }
        return jsonify(result), 200

    @staticmethod
    def updateStatus(rid, json):
        valid_parameters = Utilities.verify_parameters(json, ['fulfiller_id', 'status_id'])
        if valid_parameters:
            try:
                updatedRequest = Requests.updateStatus(rid, **valid_parameters)
                result = {
                    "message": "Success!",
                    "part": Utilities.to_dict(updatedRequest)
                }
                RequestsHandler.__sendRequestStatusEmail(rid, json)
                return jsonify(result), 200
            except Exception as e:
                print(e)
                return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def __sendRequestStatusEmail(rid, json):
        request = RequestsHandler.getRequestDictById(rid)
        part_requested = PartsHandler.getPartDictById(request['part_id'])
        requester_email = UsersHandler.getUserDictById(request['requester_id'])['email']
        status = StatusHandler.getStatusNameById(json['status_id'])

        subject = "RUMAir Inventory: Request Status Updated"
        message = Message(
            subject, recipients=[requester_email]
        )
        message.body = f"Your request for {request['quantity']} {part_requested['name']}(s) has been {status}."
        if part_requested['stock'] == 0:
            RequestsHandler.__sendPartRanOutEmail(part_requested['part_id'])
        mail.send(message)

    @staticmethod
    def __sendPartRanOutEmail(part_id):
        part_requested = PartsHandler.getPartDictById(part_id)
        leader_emails = UsersHandler.getLeaderEmails()
        subject = "RUMAir Inventory: Part out of stock"
        message = Message(
            subject, recipients=leader_emails
        )
        message.body = f"{part_requested['name']} is out of stock."

        mail.send(message)

    @staticmethod
    def addAmountUsed(rid, json):
        valid_parameters = Utilities.verify_parameters(json, ['amount_used'])
        if valid_parameters:
            try:
                updatedRequest = Requests.addAmountUsed(rid, json['amount_used'])
                result = {
                    "message": "Success!",
                    "part": Utilities.to_dict(updatedRequest)
                }
                return jsonify(result), 200
            except Exception as e:
                return jsonify(reason="Server error", error=e.__str__()), 500
