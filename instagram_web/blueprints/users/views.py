from flask import Blueprint, render_template, request,redirect,url_for,flash
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app import app
from config import S3_BUCKET,S3_LOCATION
from models.profile_page import ProfilePage

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


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_or_none(User.id == id)
    if not user:
       return redirect('login.html')
    else:
        return render_template('edit.html', user=user)

@users_blueprint.route('/edit', methods=['POST'])
def update():
    upd = User.update(username=request.form['username'],email=request.form['email']).where(User.id==current_user.id)
    upd.execute()
    flash('Your detail has been updated.')
    return redirect(url_for('users.edit' ,id=current_user.id))

@users_blueprint.route('/profile', methods=["GET"])
# @login_required
def profile():
    pp = ProfilePage.select().where(ProfilePage.user_id == current_user.id)
    return render_template('profile.html', pp=pp, s3=S3_LOCATION ,user = User.get_or_none(User.id == current_user.id) )

from helpers import *
 

@users_blueprint.route("/upload", methods=["POST"])
def upload_profile_image():

    if "user_file" not in request.files:
        flash("No user_file key in request.files")
        return redirect(url_for("users.edit" ,id=current_user.id))

    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

    if file.filename == "":
        return "Please select a file"


    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)       
        output = upload_file_to_s3(file, S3_BUCKET)
        flash('Successfully update your profile picture')       
        profile_pic_update=User.update(profile_image=file.filename).where(User.id==current_user.id)
        profile_pic_update.execute()
        return redirect(url_for("users.edit" ,id=current_user.id))

    else:
        flash('Unsuccessful upload!')
        return redirect("/")
    
@users_blueprint.route("/post", methods=['GET'])
def post():
    return render_template('for_posting.html')

@users_blueprint.route("/post", methods=['POST'])
def posting():
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

    if file.filename == "":
        return "Please select a file"


    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)       
        output = upload_file_to_s3(file, S3_BUCKET)  

        post_update = ProfilePage(posted_image=file.filename, user_id=current_user.id)
        if post_update.save():
            flash('Posted successfully')  
            return redirect(url_for('home'))
        else:
            return render_templates("for_posting.html")
        pass
            

    else:
        flash('Unsuccessful upload!')
        return redirect("/")

    
