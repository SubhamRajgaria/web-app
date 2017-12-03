#    Copyright (C) 2017 Guillaume Bernard <contact.guib@guillaume-bernard.fr>
#
#   This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, render_template
from flask_babel import Babel
from flask_breadcrumbs import Breadcrumbs
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
babel = Babel(app)
db = SQLAlchemy(app)
Breadcrumbs(app=app)


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


from webapp.home.controllers import home
from webapp.users.controllers import users
from webapp.tweets.controllers import tweets
from webapp.configuration.controllers import configuration

app.register_blueprint(home)
app.register_blueprint(users)
app.register_blueprint(tweets)
app.register_blueprint(configuration)

db.create_all()
db.create_all(bind='non-persistent-configuration')


@babel.localeselector
def get_locale():
    return 'fr'
