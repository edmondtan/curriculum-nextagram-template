from flask_wtf.csrf import CSRFProtect
from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
# from instagram_web.blueprints.follows.views import follows_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
import os
from .util.google_oauth import oauth
import config


oauth.init_app(app)

csrf = CSRFProtect(app)

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
# app.register_blueprint(follows_blueprint, url_prefix="/follows" )


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route("/")
def home():
    from models.user import User
    users = User.select()
    return render_template('home.html', users=users)







