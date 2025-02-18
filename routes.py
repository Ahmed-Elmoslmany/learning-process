from app import app
import controllers.candidates as candidates
from flask import request

@app.route('/bing')
def bing():
    return 'bong!'

@app.route('/candidates/<int:id>')
def get_candidate(id):
    return candidates.CandidateController.get_candidates(id)

@app.route('/candidates', methods =['POST'])
def create_candidate():
    if request.args.get('extension') == 'csv':
        return candidates.CandidateController.handle_candidates_report()
    return candidates.CandidateController.create_candidates()