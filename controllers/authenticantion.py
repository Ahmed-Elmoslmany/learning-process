from werkzeug.security import generate_password_hash, check_password_hash
import http
import re
import services.utils.exceptions as exc
import services.utils.token as tk
import crud_operator as co
import models.model as model
import flask as fl
from attrdict import AttrDict

class RegisterationController:
    def __init__(self, request):
        self._request = request
        self._json_body = request.get_json()
        
    @property
    def validator(self):
        return _UserRegisterationValidator

    @property
    def business_handler(self):
        return _UserBusinessHandler()
    
    @property
    def error_serializer(self):
        return exc.ErrorSerializer
    
    @property
    def serializer(self):
        return _UserSerializer

    def register(self):
        try:
            self.validator().validate(self._json_body)
            user = self.business_handler.post(self._json_body)
            return self.serializer(user).serialize(self._request.path), http.HTTPStatus.CREATED
        except exc.RequiredInputError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST   
        except exc.InvalidInputError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST
        except exc.RecordAlreadyExistError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST
        except exc.CrudOperatorError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST
        
        
class LoginController:
    def __init__(self, request):
        self._request = request
        self._json_body = request.get_json()
        self.email = self._json_body.get('email')
    
    @property
    def validator(self):
        return _UserLoginValidator
    
    @property
    def business_handler(self):
        return _UserBusinessHandler()
    
    @property
    def error_serializer(self):
        return exc.ErrorSerializer
    
    @property
    def serializer(self):
        return _UserSerializer
    
    def login(self):
        try:
            self.validator().validate(self._json_body)
            user, access_token, refresh_token = self.business_handler.get(self._json_body)
            return self.serializer(user).serialize(self._request.path, access_token, refresh_token), http.HTTPStatus.OK
        except exc.RequiredInputError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST   
        except exc.InvalidInputError as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST
        except exc.RecordNotFound as e:
            return self.error_serializer(e._message).serialize(self._request.path), http.HTTPStatus.BAD_REQUEST


class RefreshTokenController:
    def __init__(self, request):
        self._request = request
        self._token = request.get_json().get('refresh_token')
        self._roles = ['user', 'admin']
        
    @property
    def refresh(self):
        return tk.TokenService
    
    @property 
    def error_serializer(self):
        return exc.ErrorSerializer
    
    @property
    def serializer(self):
        return _AccessTokenSerializer
    
    def refresh_token(self):
        try:
            userDic = self.refresh(self._token, self._roles).token_verify()
            print(userDic)
            userObj = AttrDict(userDic)
            access_token = self.refresh().access_token(userObj)
            return self.serializer(access_token).serialize(self._request.path), http.HTTPStatus.OK
        except exc.AuthorizationError as e:
            return self.error_serializer(e._message).serialize(self._request.path), e._status
    
    
class _UserRegisterationValidator:
    def __init__(self):
        self._requires_attributes = ['name', 'email', 'password', 'confirmationPassword']  
    
    @property
    def email_regex(self):
        return '[^@]+@[^@]+\.[^@]+'
        
    def validate(self, json_body):
        self._check_required(json_body)    
        self._check_email(json_body.get('email'))
        self._check_password_confirmation(json_body.get('password'), json_body.get('confirmationPassword'))
        
    def _check_required(self, json_body):
        for attribute in self._requires_attributes:
            if attribute not in json_body:
                raise exc.RequiredInputError(f'{attribute} is required')
    
    def _check_email(self, email):
        if not re.match(self.email_regex, email):
            raise exc.InvalidInputError(f'invalid email address')
    
    def _check_password_confirmation(self, password, password_confirmation):
        if not password == password_confirmation:
            raise exc.InvalidInputError('password not match confirmation password')
    

class _UserLoginValidator:
    def __init__(self):
        self._requires_attributes = ['email', 'password']  
    
    @property
    def email_regex(self):
        return '[^@]+@[^@]+\.[^@]+'
    
    def validate(self, json_body):
        self._check_required(json_body) 
        self._check_email(json_body.get('email'))

    def _check_required(self, json_body):
        for attribute in self._requires_attributes:
            if attribute not in json_body:
                raise exc.RequiredInputError(f'{attribute} is required')
            
    def _check_email(self, email):
        if not re.match(self.email_regex, email):
            raise exc.InvalidInputError(f'invalid email address')   
        
    
class _UserSerializer:
    def __init__(self, user):
        self._user = user

    def serialize(self, path, access_token = None, refresh_token = None):
        response = {
            "path": path,
            "name": self._user.name,
            "email": self._user.email
        }
        
        if access_token:
            response['access_token'] = access_token
            response['refresh_token'] = refresh_token
            
        return response


class _AccessTokenSerializer:
    def __init__(self, access_token):
        self._access_token = access_token
        
    def serialize(self, path):
        return {
            "path": path,
            "access_token": self._access_token
        }    


class _HashingUserPasswordHandler:
    def __init__(self, json_body):
        self._json_body = json_body
        
    def generate_hashed_user_password(self):
        hashed_password = generate_password_hash(self._json_body.get('password'))    
        return hashed_password

    def check_hashed_password(self, user_password):
        if not check_password_hash(user_password, self._json_body.get('password')):
            raise exc.InvalidInputError('invalid email or password')
        
        
class _UserSanitizer:
    def __init__(self, json_body):
        self._json_body = json_body
        
    def sanitize(self):
        self._sanitize_user_role()
        self._sanitize_user_confirmation_password()
        return self._json_body
        
    def _sanitize_user_role(self):
        if 'role' in self._json_body:
            self._json_body.pop('role')
    
    def _sanitize_user_confirmation_password(self):
        if 'confirmationPassword' in self._json_body:
            self._json_body.pop('confirmationPassword')    
            

class _UserBusinessHandler:
    def __init__(self):
        self._operator = co.CurdOperator(model.User)        
        
    @property
    def sanitizer(self):
        return _UserSanitizer
    
    @property
    def hashing_handler(self):
        return _HashingUserPasswordHandler 
    
    @property
    def token_handler(self):
        return tk.TokenService   
        
    def post(self, json_body):
        user = self._operator.get_one(email=json_body.get('email'))
        if user:
            raise exc.RecordAlreadyExistError('email is already exist')
        hashed_password = self.hashing_handler(json_body).generate_hashed_user_password()
        json_body['password'] = hashed_password
        sanitized_user = self.sanitizer(json_body).sanitize()
        created_user = self._operator.create(sanitized_user)
        return created_user
    
    def get(self, json_body):
        user = self._operator.get_one(email=json_body.get('email'))
        if not user:
            raise exc.RecordNotFound('invalid email or password')
        self.hashing_handler(json_body).check_hashed_password(user.password)
        print(user)
        access_token = self.token_handler().access_token(user)
        refresh_token = self.token_handler().refresh_token(user)
        return user, access_token, refresh_token          
