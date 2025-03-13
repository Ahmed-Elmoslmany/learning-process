import services.utils.token as tk
import services.utils.exceptions as exc


class AdminAuth:
    def admin_auth_required(self, func):
        def admin_decorator():
            try:
                tk.TokenService().token_validation('admin')
            except exc.AuthorizationError as e:
                return exc.ErrorSerializer(e._message).serialize(e._path), e._status
            return func()
        return admin_decorator    
        

class UserAuth:
    def user_auth_required(self, func):
        def user_decorator():
            try:
                tk.TokenService().token_validation('user')
            except exc.AuthorizationError as e:
                return exc.ErrorSerializer(e._message).serialize(e._path), e._status
            return func()
        return user_decorator       