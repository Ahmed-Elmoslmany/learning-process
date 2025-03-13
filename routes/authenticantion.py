from app import app
import flask as fl
import controllers.authenticantion as auth

@app.route('/register', methods=['POST'])
def register():
    return auth.RegisterationController(fl.request).register()

@app.route('/login', methods=['POST'])
def login():
    return auth.LoginController(fl.request).login()

@app.route('/refresh', methods=['POST'])
def refresh_token():
    return auth.RefreshTokenController(fl.request).refresh_token()