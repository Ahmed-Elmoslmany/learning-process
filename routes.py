from app import app
import controllers.candidates as candidates
from flask import request

@app.route('/bing')
def bing():
    return 'bong!'

@app.route('/candidates')
def get_candidates():
    return candidates.CandidateController.get_candidates()

@app.route('/candidates', methods =['POST'])
def create_candidate():
    return candidates.CandidateController.create_candidate()

@app.route('/candidates/<int:id>')
def get_candidate(id):
    return candidates.CandidateController.get_candidate(id)

@app.route('/candidates/<int:id>', methods=['POST'])
def handle_candidates_report(id):
    return candidates.CandidateController.handle_candidates_report(id)

@app.route('/candidates/<int:id>', methods=['DELETE'])
def delete_candidate(id):
    return candidates.CandidateController.delete_candidate(id)

@app.route('/candidates/<int:id>', methods=['PATCH'])
def update_candidate(id):
    return candidates.CandidateController.update_candidate(id)