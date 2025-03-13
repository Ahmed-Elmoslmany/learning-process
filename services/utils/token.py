import http
import jwt
import os
import services.utils.exceptions as exc
from datetime import datetime, timedelta

class TokenService:
    def __init__(self, token = None, roles = None):
        self._token = token
        self._roles = roles
        
    def token_encode(self, user, expire, fresh=False):
        if fresh:
            expiration_time = datetime.now() + timedelta(days=expire)
        else: expiration_time = datetime.now() + timedelta(minutes=expire)
    
        return jwt.encode(
            payload={
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'exp': expiration_time 
            },
            key=os.getenv('JWT_SECRET_KEY'), algorithm='HS256'
        )
        
    def access_token(self, user):
        access_token = self.token_encode(user, 30)
        return access_token
    
    def refresh_token(self, user):
        refresh_token = self.token_encode(user, 2, True)
        return refresh_token

    def token_verify(self):
        if not self._token:
            raise exc.AuthorizationError('Forbidden Access', http.HTTPStatus.FORBIDDEN)
        try:
            decoded_data = jwt.decode(self._token.split(' ')[1], os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
            if decoded_data['role'] not in self._roles:
                raise exc.AuthorizationError('Unauthorized')
            return decoded_data
        except jwt.ExpiredSignatureError:
            raise exc.AuthorizationError('Expire Token', http.HTTPStatus.BAD_REQUEST)
        except jwt.InvalidTokenError:
            raise exc.AuthorizationError('Invalid token', http.HTTPStatus.BAD_REQUEST)     
