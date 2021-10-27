from flask import jsonify
from api.dao.status import Status
from api.util.utilities import Utilities


class StatusHandler:

    @staticmethod
    def getAllStatuses():
        try:
            statuses = Status.getStatuses()
            result_list = []
            for status in statuses:
                result_list.append(Utilities.to_dict(status))
            result = {
                "message": "Success!",
                "statuses": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getStatusNameById(sid):
        try:
            status = Status.getStatusById(sid)
            status_name = Utilities.to_dict(status)['stat']
            return status_name
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500
