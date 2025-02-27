from app import app
import http

class CreateCandidateController:
    def __init__(self, request):
        self._request = request
        
    @property
    def validator(self):
        return _CreateCandidateValidator
    
    @property
    def serializer(self):
        return _CandidateSerializer   
    
    @property
    def retriver(self):
        return _CandidateRetriver
    
    def create_candidate(self):
        try:
            self.validator(self._request.get_json()).validate()
            retrived_candidate = self.retriver.get_candidate()
            return self.serializer(retrived_candidate).serialize(self._request.path), http.HTTPStatus.CREATED
        except _ErrorValidator as e:
            return _ErrorSerializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST


class _CreateCandidateValidator:
    def __init__(self, body_json):
        self._body_json = body_json
        
    def validate(self):
        self.first_name_require()
        self.last_name_require()
        self.email_require()
        
    def first_name_require(self):    
        if 'firstname' not in self._body_json:
            raise _ErrorValidator('firstname is require')
        
    def last_name_require(self):
        if 'lastname' not in self._body_json:
            raise _ErrorValidator('lastname is require')
        
    def email_require(self):
        if 'email' not in self._body_json:
            raise _ErrorValidator('email is require')
            
            
class _CandidateSerializer:
    def __init__(self, candidate):
        self._candidate = candidate
        
    def serialize(self, path):       
        return {
            "path": path,
            "data": {
                "firstName": self._candidate._firstname,
                "lastName": self._candidate._lastname,
                "email": self._candidate._lastname
            }
        }
    

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


class _ErrorValidator(Exception):
    def __init__(self, message):
        self._message = message
        

class _CandidateRetriver:
    def get_candidate():
        return _Candidate('ahmed', 'elmoslmany', 'ahmedelmoslmany74@gmail.com')
    
    
class _Candidate:
    def __init__(self, firstname, lastname, email):
        self._firstname = firstname
        self._lastname = lastname
        self._email = email
            