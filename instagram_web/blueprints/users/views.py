from flask import Blueprint, render_template, request,redirect,url_for,flash
from models.user import User
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template('sign_up.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form.get('password')
    hashed_password = generate_password_hash(user_password)

    u=User( username=request.form.get('name'),
    email=request.form.get('email'),
    password=hashed_password
    )
    if u.save():
        flash('Successfully SIGN UP')
        return redirect(url_for('sessions.new'))
    else:
        return render_templates("sign_up.html", name=request.args['name'])
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/edit', methods=['GET'])
def edit():
    return render_template('edit.html')

@users_blueprint.route('/edit', methods=['POST'])
def update():
    upd = User.update(username=request.form['username'],email=request.form['email']).where(User.id==current_user.id)
    upd.execute()
    flash('Your detail has been updated.')
    return redirect(url_for('users.edit'))

@users_blueprint.route('/profile')
# @login_required
def profile():
    return render_template('profile.html')

    
