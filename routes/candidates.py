from app import app
import controllers.candidates as candidates
import flask as fl

@app.route('/candidates', methods=['GET'])
def get_candidates():
    return candidates.GetAllCandidatesController(fl.request).get_candidates()

@app.route('/candidates/<int:id>', methods=['GET'])
def get_candidate(id):
    return candidates.GetCandidateController(fl.request).get_candidate(id)

@app.route('/candidates', methods =['POST'])
def create_candidate():
    return candidates.CreateCandidateController(fl.request).create_candidate()

@app.route('/candidates/<int:id>', methods=['PUT'])
def update_candidate(id):
    return candidates.UpdateCandidateController(fl.request).update_candidate()

@app.route('/candidates/<int:id>', methods=['DELETE'])
def delete_candidate(id):
    return candidates.DeleteCandidateContoller(fl.request).delete_candidate()
