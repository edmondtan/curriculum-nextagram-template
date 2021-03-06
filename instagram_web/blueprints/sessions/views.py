from flask import Blueprint, render_template, request,redirect,url_for,flash ,session
from models.user import User
from werkzeug.security import check_password_hash
from app import login_manager
from flask_login import login_user,logout_user,login_required
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('login.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    username_to_check = request.form.get('username')
    password_to_check = request.form.get('password')
    
    user = User.get_or_none(User.username == username_to_check)
    
    if not user:
        flash("User doesn't exist")
        return redirect(url_for('sessions.new'))
    
    if not check_password_hash(user.password, password_to_check):
        flash("Incorrect password")
        return redirect(url_for('sessions.new') )

    else :
        flash(f"{username_to_check}, login successfully")
        login_user(user,force=True)
        return redirect(url_for('home'))

@sessions_blueprint.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('sessions.new'))

# sign in with Google
@sessions_blueprint.route('/google_login/authorize', methods=['GET'])
def authorize():
    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

        user = User.get_or_none(User.email == email)
        if not user:
            flash('invalid user')
            return redirect(url_for("sessions.new"))
    login_user(user)
    return redirect(url_for('sessions.google_login'))

@sessions_blueprint.route("/google_login", methods=['GET'])
def google_login():
    return oauth.google.authorize_redirect(url_for('sessions.authorize', _external=True))



