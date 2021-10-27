from flask import jsonify
from api.dao.parts import Parts
from api.util.utilities import Utilities


class PartsHandler:

    @staticmethod
    def getAllParts():
        try:
            parts = Parts.getParts()
            result_list = []
            for part in parts:
                result_list.append(Utilities.to_dict(part))
            result = {
                "message": "Success!",
                "parts": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getPartById(pid):
        try:
            part = Parts.getPartById(pid)
            part_dict = Utilities.to_dict(part)
            result = {
                "message": "Success!",
                "part": part_dict
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getPartDictById(pid):
        try:
            part = Parts.getPartById(pid)
            part_dict = Utilities.to_dict(part)
            return part_dict
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getPartByName(pname):
        try:
            part = Parts.getPartByName(pname)
            part_dict = Utilities.to_dict(part)
            result = {
                "message": "Success!",
                "part": part_dict
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getPartsByDepartment(did):
        try:
            parts = Parts.getPartsByDepartment(did)
            result_list = []
            for part in parts:
                result_list.append(Utilities.to_dict(part))
            result = {
                "message": "Success!",
                "parts": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getElectronicPartsByDepartment(did):
        try:
            parts = Parts.getElectronicPartsByDepartment(did)
            result_list = []
            for part in parts:
                result_list.append(Utilities.to_dict(part))
            result = {
                "message": "Success!",
                "parts": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getSoftwarePartsByDepartment(did):
        try:
            parts = Parts.getSoftwarePartsByDepartment(did)
            result_list = []
            for part in parts:
                result_list.append(Utilities.to_dict(part))
            result = {
                "message": "Success!",
                "parts": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def getNormalPartsByDepartment(did):
        try:
            parts = Parts.getNormalPartsByDepartment(did)
            result_list = []
            for part in parts:
                result_list.append(Utilities.to_dict(part))
            result = {
                "message": "Success!",
                "parts": result_list
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def createOrUpdatePart(json):
        existingPart = Parts.getPartByName(json['name'])
        if(existingPart and existingPart.dept_id == json['dept_id']):
            json["stock"] = int(json["stock"]) + int(existingPart.stock)
            return PartsHandler.updateStock(existingPart.part_id, json)
        else:
            return PartsHandler.createPart(json) 

    @staticmethod
    def createPart(json):
        valid_parameters = Utilities.verify_parameters(json, ['name', 'stock', 'dept_id', 'is_electronic', 'is_software'])
        if valid_parameters:   
            try:
                newPart = Parts(**valid_parameters).create()
                result = {
                    "message": "Success!",
                    "part": Utilities.to_dict(newPart)
                }
                return jsonify(result), 200
            except Exception as e:
                return jsonify(message="Server error", error=e.__str__()), 500
        else:
            return jsonify(message="Invalid parameters"), 400

    @staticmethod
    def deletePart(pid):
        deletedPart = Parts.delete(pid)
        if deletedPart:
            result = {
                "message": "Deleted!",
                "part": Utilities.to_dict(deletedPart)
            }
            return jsonify(result), 200
        else:
            return jsonify(message="Part not found."), 404

    @staticmethod
    def updateStock(pid, json):
        valid_parameters = Utilities.verify_parameters(json, ['stock'])
        if valid_parameters:
            try:
                updatedPart = Parts.updateStock(pid, json['stock'])
                result = {
                    "message": "Success!",
                    "part": Utilities.to_dict(updatedPart)
                }
                return jsonify(result), 200
            except Exception as e:
                return jsonify(message="Server error", error=e.__str__()), 500

    @staticmethod
    def updatePart(pid, json):
        valid_parameters = Utilities.verify_parameters(json, ['name', 'stock', 'dept_id', 'is_electronic', 'is_software'])
        if valid_parameters:
            try:
                updatedPart = Parts.updatePart(pid, **valid_parameters)
                result = {
                    "message": "Success!",
                    "part": Utilities.to_dict(updatedPart)
                }
                return jsonify(result), 200
            except Exception as e:
                return jsonify(message="Server error", error=e.__str__()), 500
