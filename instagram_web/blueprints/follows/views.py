# from flask import Blueprint,redirect, url_for, flash
# from flask_login import login_required, current_user
# from models.user import User
# from models.followerfollowing import FollowerFollowing

# follows_blurprint = Blueprint('follows',__name__, template_folder='templates')

# @follows_blueprint.route('/<idol_id>',methods=['POST'])
# @login_required
# def create(idol_id):
#     idol = User.get_or_none(User.id == idol_id)

#     if not idol:
#         flash('No user found with this id!', 'warning')
#         return redirect(url_for('home'))

#     new_follow = FollowerFollowing(
#         fan_id = current_user.id,
#         idol_id =idol.id
#     )
#     if not idol.is_private:
#         new_follow.approved = True

#     if not new_follow.save():
#         flash('Unable to follow this user')
#         return redirect(url_for('user.show', username=idol.username))

#     if new_follow.is_approved:
#         flash('You are now following {idol.username}!','success')
#         return redirect(url_for('users.show',username=idol.username))

#     flash('Follow request sent! Please wait for approval!', 'success')
#     return redirect(url_for('users.show', username=idol.username))