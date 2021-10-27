from flask import jsonify, session
from api.dao.tools import Tools
from api.util.utilities import Utilities


class ToolsHandler:

    @staticmethod
    def getTools():
        try:
            tools = Tools.getTools()
            result_list = []
            for tool in tools:
                result_list.append(Utilities.raw_sql_to_dict(tool))
            result = {
                "message": "Success!",
                "result": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getAllTools():
        try:
            tools = Tools.getAllTools()
            columns = ['name','category','image','id']
            result_list = []
            for tool in tools:
                tool_dict = {}
                for i in range(len(columns)):
                    tool_dict[columns[i]] = tool[i]
                result_list.append(tool_dict)
            result = {
                "message": "Success!",
                "result": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500
            
    @staticmethod
    def getToolById(tid):
        try:
            tools = Tools.getToolById(tid)
            result_tool = []
            for tool in tools:
                result_tool = (Utilities.raw_sql_to_dict(tool))
            result = {
                "message": "Success!",
                "result": result_tool
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500
    
    #create tool
    @staticmethod
    def createTool(tool):
        try:
            queryResponse = Tools.createTool(tool)
            result = {
                "message": "Success!",
                "response": queryResponse
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    #update tool
    @staticmethod
    def updateTool(tool):
        try:
            queryResponse = Tools.updateTool(tool)
            result = {
                "message": "Success!",
                "response": queryResponse
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    #delete tool
    @staticmethod
    def deleteTool(tool_id):
        try:
            queryResponse = Tools.deleteTool(tool_id)
            result = {
                "message": "Success!",
                "response": queryResponse
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500
    
    @staticmethod
    def getToolTable():
        try:
            tools = Tools.getToolTable()
            columns = ['id','name','category','image','status','comment','user_id','user_name','report_id','report_date']
            result_list = []
            for tool in tools:
                tool_dict = {}
                for i in range(len(columns)):
                    tool_dict[columns[i]] = tool[i]
                result_list.append(tool_dict)
            result = {
                "message": "Success!",
                "result": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500

    @staticmethod
    def getToolsFromUser(user_id):
        try:
           tools = Tools.getToolsFromUser(user_id)
           columns = ['id','name','category','image']
           result_list = []
           for tool in tools:
                tool_dict = {}
                for i in range(len(columns)):
                    tool_dict[columns[i]] = tool[i]
                result_list.append(tool_dict)
                result = {
                "message": "Success!",
                "result": result_list
            }
           return jsonify(result), 200
        except Exception as e:
            return jsonify(reason="Server error", error=e.__str__()), 500
