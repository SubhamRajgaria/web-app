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

from flask_babel import _
from wtforms import Form, StringField, validators, IntegerField, PasswordField, SubmitField, HiddenField


class NewStudyForm(Form):
    """
    This form defines the parameters to register a new study
    name : name of study
    description : description of the study
    user_db_host : host IP address
    user_db_port : Port address
    user_db_name : Database name
    user_db_password : password of database
    tweets_db_host : host of tweets database
    tweets_db_port : port of tweets database
    tweets_db_name : Name of tweets database
    register : Button to register the study
    update : Button to update the study name
    
    """
    id = HiddenField("id")

    name = StringField(_("Name"), [
        validators.Length(max=255, message=_("Length of the study name is limited up to 255 characters.")),
        validators.DataRequired(message=_("This field is required")),
    ], render_kw={"placeholder": "La Rochelle"})

    description = StringField(_("Description"), [
        validators.Length(max=255, message=_("Length of the study description is limited up to 255 characters.")),
        validators.Optional()
    ], render_kw={"placeholder": "A study about La Rochelle inhabitants"})

    user_db_host = StringField(_("Host (name or IP)"), [
        validators.DataRequired(message=_("This field is required")),
    ], render_kw={"placeholder": "127.0.0.1 or mysql.domain.tld"})

    user_db_port = IntegerField(_("Port number"), [
        validators.NumberRange(min=0, max=65535, message="A port number is greater than 0 and lower than 65535"),
        validators.DataRequired(message=_("This field is required")),
    ], default=3306)

    user_db_name = StringField(_("Database Schema"), [
        validators.DataRequired(message=_("This field is required")),
    ], render_kw={"placeholder": "larochelle"})

    user_db_user = StringField(_("Username"), [
        validators.DataRequired(message=_("This field is required")),
    ])

    user_db_password = PasswordField(_("User password"), [
        validators.DataRequired(message=_("This field is required")),
    ])

    tweets_db_host = StringField(_("Host (name or IP)"), [
        validators.DataRequired(message=_("This field is required")),
    ], render_kw={"placeholder": "127.0.0.1 or mongo.domain.tld"})

    tweets_db_port = IntegerField(_("Port number"), [
        validators.NumberRange(min=0, max=65535, message="A port number is greater than 0 and lower than 65535"),
        validators.DataRequired(message=_("This field is required")),
    ], default=27017)

    tweets_db_name = StringField(_("Database Collection"), [
        validators.DataRequired(message=_("This field is required")),
    ])

    register = SubmitField(_("Register"), [
        validators.Optional()
    ])

    update = SubmitField(_("Update"), [
        validators.Optional()
    ])

class DeleteStudyForm(Form):
    """
    id: Hidden field which is rendered with delete button
    delete : button to delete a study
    """
    id = HiddenField("id")
    delete = SubmitField(_("Delete"), [
        validators.Optional()
    ])

class ConnectStudyForm(Form):
    """
       id: Hidden field which is rendered with delete button
       connect : button to connect a study
       disconnect : button to disconnect a study
       """
    id = HiddenField("id")
    connect = SubmitField(_("Connect"), [
        validators.Optional()
    ])
    disconnect = SubmitField(_("Disconnect"), [
        validators.Optional()
    ])
