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


class Filter(Form):
    """
    Form for filtering users
    :param id : Hidden id
    :param name : Name to be filtered
    :type str
    :param register : A button to include the name
    :param unregister : a button to exclude the name
    :param delete : To delete a filter(the functionality has been kept inactive)
    
    """
    id = HiddenField("id")
    entries = []

    name = StringField(_("Name"), [
        validators.Length(max=255),
        validators.Optional(),
        validators.Regexp(regex="[a-zA-Z0-0]+")
    ], render_kw={"placeholder": "Filter"})

    register = SubmitField(_("Include"), [
        validators.Optional()
    ])

    unregister = SubmitField(_("Exclude"), [
        validators.Optional()
    ])

    delete = SubmitField(_("Delete"),[
        validators.Optional()
    ])

class Exclude(Form):
    """
    A form to exclude users from a study
    
    :param selected_users : To keep a track of all the selected users
    :param exclude_temporary : To maintain a list of users which have been selected to exclude
    :param exclude_permanent : To maintain a list of users which are excluded permanently
    :param present_counts : To maintain a list of the number of users selected to exclude
    :param excludeTemporary : Button to exclude users in exclude_temporary
    :param excludePermanent : Button to exclude users in selected users permanently
    
    """
    selected_users = []
    exclude_temporary = []

    exclude_permanent = []

    present_counts = []

    excludeTemporary = SubmitField(_("Exclude Temporarily"), [
        validators.Optional()
    ])

    excludePermanent = SubmitField(_("Exclude Permanently"), [
        validators.Optional()
    ])

class Save(Form):
    """
    A form to save the filters and exclusions
    
    :param nameOfSearch : name of the search
    :type str
    :param description : description of the search performed
    :type : str
    :param saveFilters : To save the search with name and description
    :param exportSavedFilters : To load a previously saved filter
    :param findName : Text field to allow to search past saved filters
    
    """
    id = HiddenField("id")
    nameOfSearch = StringField(_("Name"), [
        validators.Length(max=255),
        validators.Optional()
    ], render_kw={"placeholder": "A filter to do ...."})

    description = StringField(_("Description"), [
        validators.Length(max=255),
        validators.Optional()
    ], render_kw={"placeholder": "A filter to do ...."})

    saveFilters = SubmitField(_("Save"), [
        validators.Optional()
    ])

    exportSavedFilters = SubmitField(_("Load this search"), [
        validators.Optional()
    ])

    findName = StringField(_("Choose Past Search"), [
        validators.Length(max=255),
        validators.Optional()
    ], render_kw={"placeholder": "Past Saved Searches"})

    removeAllFilters = SubmitField(_("Remove all filters"), [
        validators.Optional()
    ])


"""class ExportData(Form):
    id = HiddenField("id")
    saveUsers = SubmitField(_("Save this Search and get tweets"), [
        validators.Optional()
    ])"""

class downloadForm(Form):
    """
    A form for the download dialog box which pops when you have to download tweets
    
    :param name : Name by which you want to download the file
     :type str
     :param download : A button to submit the download
    """
    id = HiddenField("id")

    name = StringField(_("Name"), [
        validators.Length(max=255, message=_("Length of the download name is limited up to 255 characters.")),
        validators.DataRequired(message=_("This field is required")),
    ], render_kw={"placeholder": "User_tweets"})

    download = SubmitField(_("Download"), [
        validators.Optional()
    ])




