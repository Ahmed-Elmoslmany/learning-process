from app import app
import http
import csv
import os
import re
import datetime
import crud_operator as co
import models.model as model
import services.utils.exceptions as exc
import services.utils.token as tk
import jwt


class GetAllCandidatesController:
    def __init__(self, request):
        self._request = request
        
    @property
    def serializer(self):
        return _CandidatesCollectionSerializer
    
    @property
    def business_handler(self):
        return co.CurdOperator(model.Candidate)
    
    def get_candidates(self):
        retrieved_candidates = self.business_handler.get_all()
        print(retrieved_candidates)
        return self.serializer(retrieved_candidates).serialize(self._request.path), http.HTTPStatus.OK
    

class GetCandidateController:
    def __init__(self, request):
        self._request = request

    @property
    def serializer(self):
        return _CandidateSingleSerializer
    
    @property
    def error_serializer(self):
        return exc.ErrorSerializer
    
    @property
    def business_handler(self):
        return co.CurdOperator(model.Candidate)
    
    def get_candidate(self, id):
        try:
            retrieved_candidate = self.business_handler.get_by_id(id)
            return self.serializer(retrieved_candidate).serialize(self._request.path), http.HTTPStatus.OK
        except exc.RecordNotFound as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST

    
class CreateCandidateController:
    def __init__(self, request):
        self._request = request
        self._token = request.headers.get('Authorization')
        self._json_body = request.get_json()
    
    @property
    def validator(self):
        return _CreateCandidateValidator()
    
    @property
    def business_handler(self):
        return co.CurdOperator(model.Candidate)
        
    @property
    def serializer(self):
        return _CandidateSingleSerializer    

    @property
    def error_serializer(self):
        return exc.ErrorSerializer
    
    @property
    def data_base_error_serializer(self):
        return exc.CrudOperatorErrorSerializer
    
    def create_candidate(self):
        try:
            self.validator.validate(self._json_body, self._token)
            created_candidate = self.business_handler.create(self._json_body)
            return self.serializer(created_candidate).serialize(self._request.path), http.HTTPStatus.CREATED
        except exc.AuthorizationError as e:
            return self.error_serializer(e._message).serialize(self._request.path), e._status
        except exc.RequiredInputError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST
        except exc.InvalidInputError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST
        except exc.CrudOperatorError as e:
            return self.data_base_error_serializer(e._message, e._method ).serialize(self._request.path), http.HTTPStatus.INTERNAL_SERVER_ERROR
        
        
class UpdateCandidateController:
    def __init__(self, request):
        self._request = request
        self._token = request.headers.get('Authorization')
        self._json_body = request.get_json()
    
    @property
    def validator(self):
        return _UpdateCandidateValidator()
    
    @property    
    def serializer(self):
        return _CandidateSingleSerializer  

    @property
    def business_handler(self):
        return co.CurdOperator(model.Candidate)
    
    @property
    def error_serializer(self):
        return exc.ErrorSerializer
    
    def update_candidate(self, id):
        try:
            self.validator.validate(self._json_body, self._token)
            retrieved_candidate = self.business_handler.update(id, self._json_body)
            return self.serializer(retrieved_candidate).serialize(self._request.path), http.HTTPStatus.OK
        except exc.AuthorizationError as e:
            return self.error_serializer(e._message).serialize(self._request.path), e._status
        except exc.RecordNotFound as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.NOT_FOUND


class DeleteCandidateController:
    def __init__(self, request):
        self._request = request
        self._token = request.headers.get('Authorization')

    @property
    def validator(self):
        return _DeleteCandidateValidator()
    
    @property
    def serializer(self):
        return _MessageSerializer
    
    @property
    def business_handler(self):
        return co.CurdOperator(model.Candidate)
    
    @property
    def error_serializer(self):
        return exc.ErrorSerializer
    
    def delete_candidate(self, id):
        try:
            self.validator.validate(self._token)
            deletion_success = self.business_handler.delete(id)
            if deletion_success:
                return self.serializer('record deleted').serialize(self._request.path), http.HTTPStatus.RESET_CONTENT 
            return self.error_serializer('record not found').serialize(self._request.path), http.HTTPStatus.NOT_FOUND
        except exc.AuthorizationError as e:
            return self.error_serializer(e._message).serialize(self._request.path), e._status
        except exc.RecordNotFound as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.NOT_FOUND 


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
    def __init__(self):
        self._requires_attributes = ['first_name', 'last_name', 'email', 'age', 'date_of_birth']
        self._roles = ['admin']
        
    @property
    def token_validator(self):
        return tk.TokenService
        
    @property
    def email_regex(self):
        return '[^@]+@[^@]+\.[^@]+'
    
    @property
    def first_name_regex(self):
        return '^\w{3,32}$'
    
    @property
    def last_name_regex(self):
        return '^\w{3,32}$'
    
    @property
    def date_of_birth_regex(self):
        return '^\d{2}-\d{2}-\d{4}$'
    
    def validate(self, json_body, token):
        self._check_token(token)
        self._check_required(json_body)
        self._check_email(json_body.get('email'))
        self._check_first_name(json_body.get('first_name'))    
        self._check_last_name(json_body.get('last_name'))    
        self._check_age(json_body.get('age'))
        self._check_birth_date(json_body.get('date_of_birth'))
        
    def _check_required(self, json_body):
        for attribute in self._requires_attributes:
            if attribute not in json_body:
                raise exc._RequiredInputError(f'{attribute} is required')

    def _check_email(self, email):
        if not re.match(self.email_regex, email):
            raise exc.InvalidInputError(f'invalid email address')

    def _check_first_name(self, first_name):
        if not isinstance(first_name, str) or not re.match(self.first_name_regex, first_name):
            raise exc.InvalidInputError('invalid first name')
    
    def _check_last_name(self, last_name):
        if not isinstance(last_name, str) or not re.match(self.last_name_regex, last_name):
            raise exc.InvalidInputError('invalid last name')
        
    def _check_age(self, age):
        if not isinstance(age, int) or int(age) < 16 or int(age) > 80:
            raise exc.InvalidInputError('invalid age')
        
    def _check_birth_date(self, date_of_birth):
        date = date_of_birth.split('-') #use regex
        if not re.match(self.date_of_birth_regex, date_of_birth) or date[0] > '31' or date[1] > '12' or date[2] > str(datetime.datetime.now().year - 16):
            raise exc.InvalidInputError('invalid birth date')
    
    def _check_token(self, token):
        self.token_validator(token, self._roles).token_verify()


class _UpdateCandidateValidator:
    def __init__(self):
        self._requires_attributes = ['first_name', 'last_name', 'email', 'age', 'date_of_birth']
        self._roles = ['admin']
        
    @property
    def token_validator(self):
        return tk.TokenService
    
    def validate(self, json_body, token):
        self._check_token(token)
    
    def _check_token(self, token):
        self.token_validator(token, self._roles).token_verify()    


class _DeleteCandidateValidator:
    def __init__(self):
        self._roles = ['admin']
        
    @property
    def token_validator(self):
        return tk.TokenService
    
    def validate(self, token):
        self._check_token(token)
    
    def _check_token(self, token):
        self.token_validator(token, self._roles).token_verify() 
    
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
            "lastName": self._candidate.last_name,
            "email": self._candidate.email,
            "age": self._candidate.age,
            "dateOfBirth": self._candidate.date_of_birth,
            
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


class _MessageSerializer:
    def __init__(self, message):
        self._message = message
    
    def serialize(self, path):
        return {
            "path": path,
            "message": self._message
            
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
        