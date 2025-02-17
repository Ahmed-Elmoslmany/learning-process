from app import app
import controllers.candidates as candidates

@app.route('/bing')
def bing():
    return 'bong!'

@app.route('/candidate/<int:id>')
def get_candidate(id):
    return candidates.CandidateController.get_candidates(id)

@app.route('/candidate', methods =['POST'])
def create_candidate():
    return candidates.CandidateController.create_candidates()

@app.route('/candidatecsv/<int:id>', methods =['get'])
def generate_csv(id):
    return candidates.CandidateController.create_csv(id)