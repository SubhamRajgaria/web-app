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

from flask import Blueprint, render_template
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from flask_babel import _

tweets = Blueprint('tweets', __name__, url_prefix='/tweets')
default_breadcrumb_root(tweets, '.')

@tweets.route('/list', methods=['GET'])
@register_breadcrumb(tweets, '.users.tweets', _('List Tweets'))
def tweets_list():
    return render_template('tweets/list.html', title=_("List Tweets"))


@tweets.route('/export', methods=['GET'])
@register_breadcrumb(tweets, '.users.tweets.list', _('Export tweets'))
def tweets_export():
    return render_template('tweets/export.html', title=_("Export tweets"))