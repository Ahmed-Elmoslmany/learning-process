from flask import jsonify, request
from http import HTTPStatus
from services.db_service import DBService
from services.csv_service import Csv

class CandidateController():

    def get_candidates(candidate_id):
        candidate = DBService.get_candidate(candidate_id)
        return jsonify({
            "status": "success",
            "data": {
                "id": candidate.id,
                "firstname": candidate.firstname,
                "lastname": candidate.lastname,
                "email": candidate.email
            }
        }, HTTPStatus.OK)

    def create_candidates():
        data = request.get_json()

        if not data or not 'firstname' or not 'lastname' or not 'email' in data:
            return jsonify({
                "status": "Fail",
                "data": {
                    "message": "firstname, lastname and email is required"
                }
            }, HTTPStatus.BAD_REQUEST)

        new_candidate = DBService.create_candidate(data)

        return jsonify({
            "status": "success",
            "data": {
                "id": new_candidate.id,
                "firstname": new_candidate.firstname,
                "lastname": new_candidate.lastname,
                "email": new_candidate.email
            }
        }, HTTPStatus.CREATED)
    

    def handle_candidates_report():
        extension = request.args.get('extension')
        if extension != 'csv' or not request.args.get('candidate_id'):
            return jsonify({
                    "status": "fail",
                    "data": {
                        "message": "Invalid extension or candidate id"
                    }
            }, HTTPStatus.BAD_REQUEST)    
        else :
            candidate = DBService.get_candidate(request.args.get('candidate_id'))
            csv = Csv(candidate.firstname, ['firstname', 'lastname', 'email'], [[candidate.firstname, candidate.lastname, candidate.email]])
            if csv.generate():
                csv_path = csv.get_file_path()
                return jsonify({
                    "status": "success",
                    "data": {
                        "path": csv_path
                    }
                }, HTTPStatus.OK)
                
            return jsonify({
                    "status": "fail",
                    "data": {
                        "message": "Error while generating the file"
                    }
            }, HTTPStatus.SERVICE_UNAVAILABLE)

    