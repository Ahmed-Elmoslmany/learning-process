from app import app
from flask import jsonify, request
from http import HTTPStatus
from services.db_service import DBService
from services.csv_service import Csv

class CandidateController():

    def get_candidates():
        candidates = DBService.get_candidates()
        serilized_candidates = [{"id": candidate.id, "firstname": candidate.firstname, "lastname": candidate.lastname, "email": candidate.email} for candidate in candidates]
        
        return jsonify({
            "status": "success",
            "data": serilized_candidates
        }, HTTPStatus.OK)
        
    def get_candidate(candidate_id):
        candidate = DBService.get_candidate(candidate_id)
        if not candidate:
            app.logger.warning('can not found candidate')
            
            return jsonify({
                    "status": "fail",
                    "data": {
                        "message": "Candidate not found"
                    }
            }, HTTPStatus.NOT_FOUND)
            
        app.logger.info(f'candidate found!, id: {candidate.id} firstname: {candidate.firstname} lastname: {candidate.lastname} email: {candidate.email}')
        
        return jsonify({
            "status": "success",
            "data": {
                "id": candidate.id,
                "firstname": candidate.firstname,
                "lastname": candidate.lastname,
                "email": candidate.email
            }
        }, HTTPStatus.OK)

    def create_candidate():
        data = request.get_json()

        if not data or not 'firstname' or not 'lastname' or not 'email' in data:
            app.logger.warning('candidate data not provided')
            return jsonify({
                "status": "fail",
                "data": {
                    "message": "firstname, lastname and email is required"
                }
            }, HTTPStatus.BAD_REQUEST)

        new_candidate = DBService.create_candidate(data)
        app.logger.info(f'candidate found!, id: {new_candidate.id} firstname: {new_candidate.firstname} lastname: {new_candidate.lastname} email: {new_candidate.email}')
        
        return jsonify({
            "status": "success",
            "data": {
                "id": new_candidate.id,
                "firstname": new_candidate.firstname,
                "lastname": new_candidate.lastname,
                "email": new_candidate.email
            }
        }, HTTPStatus.CREATED)
    
    def delete_candidate(candidate_id):
        if DBService.delete_candidate(candidate_id):
            return jsonify({
                "status": "success",
                "data": {
                    "message": "candidate deleted successfully"
            }
        }, HTTPStatus.CREATED)
        else:
            return jsonify({
                "status": "fail",
                "data": {
                    "message": "provide valid candidate id"
                }
            }, HTTPStatus.BAD_REQUEST)    
            
            
    def update_candidate(candidate_id):
        data = request.get_json()
        
        new_candidate = DBService.update_candidate(candidate_id, data)
        
        if new_candidate:
            return jsonify({
                "status": "success",
                "data": {
                    "id": new_candidate.id,
                    "firstname": new_candidate.firstname,
                    "lastname": new_candidate.lastname,
                    "email": new_candidate.email
            }
        }, HTTPStatus.OK)
        else:
            return jsonify({
                "status": "fail",
                "data": {
                    "message": "candidate not found, provide valid candidate id"
                }
            }, HTTPStatus.BAD_REQUEST)    
                
        

    def handle_candidates_report(candidate_id):
        data = request.get_json()
        print(data)
        if not 'extension' in data or data['extension'] != 'csv':
            app.logger.warning('invalid report extension or candidate id')
            
            return jsonify({
                    "status": "fail",
                    "data": {
                        "message": "Invalid extension or candidate id"
                    }
            }, HTTPStatus.BAD_REQUEST)    
        else :
            candidate = DBService.get_candidate(candidate_id)
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

    
    