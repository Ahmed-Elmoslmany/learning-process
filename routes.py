from app import app
import controllers.candidates as candidates

@app.route('/bing')
def bing():
    return 'bong!'

@app.route('/candidates/<int:id>')
def get_candidate(id):
    return candidates.CandidateController.get_candidates(id)

@app.route('/candidates', methods =['POST'])
def create_candidate():
    return candidates.CandidateController.create_candidates()

@app.route('/candidates', methods =['POST'])
def handle_candidates_report():
    return candidates.CandidateController.handle_candidates_report()