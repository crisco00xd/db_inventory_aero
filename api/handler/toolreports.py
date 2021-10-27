from flask import jsonify, session
from api.dao.toolreports import ToolReports
from api.util.utilities import Utilities


class ToolReportsHandler:

    @staticmethod
    def getToolReports(tid):
        try:
            reports = ToolReports.getToolReports(tid)
            result_list = []
            for report in reports:
                result_list.append(Utilities.raw_sql_to_dict(report))
            result = {
                "message": "Success!",
                "result": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getAllToolReports():
        try:
            toolreports = ToolReports.getAllToolReports()
            result_list = []
            for report in toolreports:
                result_list.append(Utilities.to_dict(report))
            result = {
                "message": "Success!",
                "result": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def createToolReport(report):
        try:
            queryResponse = ToolReports.createToolReport(report)
            result = {
                "message": "Success!",
                "response": queryResponse
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getLatestReport(tool_id):
        try:
            response = ToolReports.getLatestReport(tool_id)
            toolreport = None
            for report in response:
                toolreport = Utilities.raw_sql_to_dict(report)
            result = {
                "message": "Success!",
                "result": toolreport
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500
        
    @staticmethod
    def updateToolReport(tool_report):
        try:
            requestResponse = ToolReports.updateToolReport(tool_report)
            result = {
                "message": "Success!",
                "response": requestResponse
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def deleteToolReport(report_id):
        try:
            queryResponse = ToolReports.deleteToolReport(report_id)
            result = {
                "message": "Success!",
                "response": queryResponse
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500