from app import db
from models.model import Candidate

class DBService():

    @staticmethod
    def get_candidate(candidate_id):
        return Candidate.query.get(candidate_id)
    

    @staticmethod
    def create_candidate(data):
        print(data)
        new_candidate = Candidate(firstname=data['firstname'], lastname=data['lastname'], email=data['email'])
        db.session.add(new_candidate)
        db.session.commit()
        return new_candidate