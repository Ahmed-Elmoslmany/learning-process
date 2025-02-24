from app import app
import http

class GetAllCandidatesController:
    def __init__(self, request):
        self._request = request
        
    @property
    def serializer(self):
        return _CandidatesCollectionSerializer
    
    @property
    def retriever(self):
        return _CandidateRetriever()
    
    def get_candidates(self):
        retrieved_candidates = self.retriever.get_all()
        return self.serializer(retrieved_candidates).serialize(self._request.path), http.HTTPStatus.OK


class GetCandidateController:
    def __init__(self, request):
        self._request = request

    @property
    def serializer(self):
        return _CandidateSingleSerializer
    
    @property
    def retriever(self):
        return _CandidateRetriever()
    
    def get_candidate(self):
        retrieved_candidate = self.retriever.get_one()
        return self.serializer(retrieved_candidate).serialize(self._request.path), http.HTTPStatus.OK
    
    
class CreateCandidateController:
    def __init__(self, request):
        self._request = request
        
    @property
    def serializer(self):
        return _CandidateSingleSerializer    

    @property
    def retriever(self):
        return _CandidateRetriever()

    def create_candidate(self):
        retrieved_candidate = self.retriever.get_one()
        return self.serializer(retrieved_candidate).serialize(self._request.path), http.HTTPStatus.CREATED
        

class UpdateCandidateController:
    def __init__(self, request):
        self._request = request
    
    @property    
    def serializer(self):
        return _CandidateSingleSerializer  

    @property
    def retriever(self):
        return _CandidateRetriever()
    
    def update_candidate(self):
        retrieved_candidate = self.retriever.update_one()
        return self.serializer(retrieved_candidate).serialize(self._request.path), http.HTTPStatus.OK
    

class DeleteCandidateController:
    def __init__(self, request):
        self._request = request

    @property
    def serializer(self):
        return _CandidateMessageSerializer
    
    @property
    def retriever(self):
        return _CandidateRetriever()
    
    def delete_candidate(self):
        retrieved_message = self.retriever.delete_one()
        return self.serializer(retrieved_message).serialize(self._request.path), http.HTTPStatus.OK 


class _CandidateSingleSerializer:
    def __init__(self, candidate):
        self.candidate = candidate
        
    def serialize(self, path):
        return {
            "path": path,
            "data": _CandidateSerializer(self.candidate).serialize()
        }        

                    
class _CandidatesCollectionSerializer:
    def __init__(self, candidates):
        self._candidates = candidates
        
    def serialize(self, path):
        return {
            "path": path,
            "data": [_CandidateSerializer(candidate).serialize() for candidate in self._candidates ]
        }    
        
        
class _CandidateSerializer:
    def __init__(self, candidate):
        self._candidate = candidate
        
    def serialize(self):
        return {
            "firstName": self._candidate.first_name,
            "lastName": self._candidate.last_name
        }                


class _CandidateMessageSerializer:
    def __init__(self, message):
        self._message = message
    
    def serialize(self, path):
        return {
            "path": path,
            "data": {
                "message": self._message.message
            }
            
        }    


class _CandidateRetriever:
    def get_all(self):
        return [Candidate("ahmed", "elmoslmany"), Candidate("Islam", "Salem")]
        
    def get_one(self):
        return Candidate("ahmed", "elmoslmany")   
    
    def update_one(self):
        return Candidate("ahmed updated", "elmoslmany")   

    def delete_one(self):
        return Message('candidate deleted')
    
    
class Candidate:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name        


class Message:
    def __init__(self, message):
        self.message = message        
        