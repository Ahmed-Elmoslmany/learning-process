from app import app
import http
import csv
import os
import services.csv_service as cs


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
        self._json_body = request.get_json()
        
    @property
    def validator(self):
        return _CreateCandidateValidator    
        
    @property
    def serializer(self):
        return _CandidateSingleSerializer    

    @property
    def retriever(self):
        return _CandidateRetriever()

    def create_candidate(self):
        try:
            self.validator(self._json_body).validate()
            retrieved_candidate = self.retriever.get_one()
            return self.serializer(retrieved_candidate).serialize(self._request.path), http.HTTPStatus.CREATED
        except _ValidationError as e:
            return _ErrorSerializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST

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


class GenerateCandidateCSVController:
    def __init__(self, request):
        self._request = request
    
    @property
    def serializer(self):
        return _CandidateCSVSerializer
    
    @property
    def retriever(self):
        return _CandidateCSVRetriever    

    def get_csv(self):
        retrieved_candidate = Candidate("ahmed", "elmoslmany")
        csv_retriever = self.retriever(retrieved_candidate)
        csv_retriever.generate_csv()
        return self.serializer(csv_retriever.retrieve_csv_path()).serialize(self._request.path), http.HTTPStatus.OK


class _CreateCandidateValidator:
    def __init__(self, json_body):
        self._json_body = json_body
        
    @property
    def serializer(self):
        return _ErrorSerializer
    
    def validate(self):
        self.first_name_required()
        self.last_name_required()
        self.email_required()
        
    def first_name_required(self):
        if 'firstname' not in self._json_body:
            raise _ValidationError('first_name is required')
            
    def last_name_required(self):
        if 'lastname' not in self._json_body:
            raise _ValidationError('last_name is required')
    
    def email_required(self):
        if 'email' not in self._json_body:
            raise _ValidationError('email is required')


class _ValidationError(Exception):
    def __init__(self, message):
        self._message = message
    
    
class _ErrorSerializer:
    def __init__(self, message):
        self._message = message
        
    def serialize(self, path):
        return {
            "path": path,
            "data": {
                "message": self._message
            }
        }    
        
    
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


class _CandidateCSVSerializer:
    def __init__(self, csv_path):
        self._csv_path = csv_path
        
    def serialize(self, path):
        return {
            "path": path,
            "data": {
                "csvPath": self._csv_path
            }
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
    

class _CandidateCSVRetriever:
    def __init__(self, candidate):
        self._csv = CSV(candidate.first_name, ['first_name', 'last_name'], [[candidate.first_name, candidate.last_name]])
        
    def generate_csv(self):
        try:
            with open(self._csv.filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)

                csvwriter.writerow(self._csv.fields)
                csvwriter.writerows(self._csv.data)
        except:
            return False
        
    def retrieve_csv_path(self):
        return f'{os.getcwd()}/{self._csv.filename}'

    
class Candidate:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name        


class CSV:
    def __init__(self, filename, fields, data):
        self.filename = f'{filename}.csv'
        self.fields = fields
        self.data = data


class Message:
    def __init__(self, message):
        self.message = message        
        