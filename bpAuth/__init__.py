from datetime import timedelta
from flask import Blueprint, make_response, redirect, url_for, request, flash, render_template, current_app
from flask_jwt_extended import create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies
from flask_login import LoginManager, login_user, login_required, logout_user

from utils.user import userLogin, userSignup, getUserOnly


authBP = Blueprint('authBluePrint', __name__)

loginManager = LoginManager()
jwt = JWTManager()


@loginManager.user_loader
def loadUser(user_id):
    return getUserOnly(user_id)


@jwt.expired_token_loader
def refreshToken(jwt_header, jwt_data):
    response = make_response(redirect(url_for('authBluePrint.login')))
    unset_jwt_cookies(response)
    return response


@authBP.route('/login/only-collaborator', methods=['GET', 'POST'])
def loginEndPoint():
    if request.method == 'POST':
        status, user = userLogin(request.form)
        if status == 200:
            flash("Login successful")
            response = redirect(url_for('genericBluePrint.generalEndPoint'))
            set_access_cookies(response, create_access_token(identity=user.bcpId))
            response.set_cookie("preferred_update", "1")
            response.set_cookie("preferred_gameType", "1")
            response.set_cookie("preferred_language", "en")
            login_user(user)
            return response
        if status == 401:
            flash("Could not verify")
            return make_response(render_template('login.html', title="Login"), 401, {'Authentication': '"login required"'})
    return render_template('login.html', title="Login")


@authBP.route('/logout', methods=['GET', 'POST'])
@login_required
def logoutEndPoint():
    response = redirect(url_for('genericBluePrint.generalEndPoint'))
    unset_jwt_cookies(response)
    logout_user()
    flash("Logout successfully")
    return response
