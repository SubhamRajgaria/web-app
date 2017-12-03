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

from flask import Blueprint, request, render_template
from flask_babel import _
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root

from webapp.home.forms import NewStudyForm, DeleteStudyForm, ConnectStudyForm
from webapp.home.models import StudyDAO, Study

home = Blueprint('home', __name__, url_prefix='/')
default_breadcrumb_root(home, '.')


def __handle_new_study_form(new_study_form, info_messages, error_messages):
    """
    Method to handle a new form 
    
    :param new_study_form: a flask form variable
    :param info_messages: a list of messages to be displayed
    :param error_messages: list of error messages 
    :return: No return value
    """
    if new_study_form.register.data:
        StudyDAO.get_instance().save(Study.from_study_form(new_study_form))
        info_messages.append(_("New study {0} saved".format(new_study_form.name.data)))

    elif new_study_form.update.data:
        study = StudyDAO.get_instance().find(new_study_form.id.data)
        study.update_with_form(new_study_form)
        StudyDAO.get_instance().update(study)
        info_messages.append(_("Study {0} updated".format(study.name)))


def __handle_delete_study_form(delete_study_form, info_messages, error_messages):
    """
    Method to delete a study
    
    :param delete_study_form: form to be deleted
    :param info_messages: list of information messages
    :param error_messages: list of error messages
    :return: No return value
    """
    study = StudyDAO.get_instance().find(delete_study_form.id.data)
    StudyDAO.get_instance().delete(study)
    info_messages.append(_("Study {0} deleted".format(study.name)))


def __handle_connect_study_form(connect_study_form, info_messages, error_messages):
    """
    Method to establish connection
    
    :param connect_study_form: The study to be connected  
    :param info_messages: list of information messages
    :param error_messages: list of error messages
    :return: No return value
    """
    if connect_study_form.connect.data:
        study = StudyDAO.get_instance().find(connect_study_form.id.data)
        try:
            study.connect()
        except Exception as ex:
            error_messages.append(str(ex))

    if connect_study_form.disconnect.data:
        study = StudyDAO.get_instance().find(connect_study_form.id.data)
        try:
            study.disconnect()
        except Exception as ex:
            error_messages.append(str(ex))


@home.route('/', methods=['GET', 'POST'])
@register_breadcrumb(home, '.', _('Home'))
def index():
    """
    Index function for homepage of the website
    
    :return: Template of the homepage 
    """

    # The various forms
    new_study_form = NewStudyForm(request.form)
    delete_study_form = DeleteStudyForm(request.form)
    connect_study_form = ConnectStudyForm(request.form)

    error_messages = []
    info_messages = []

    if request.method == 'POST':
        if new_study_form.register.data or new_study_form.update.data:
            if new_study_form.validate():
                __handle_new_study_form(new_study_form, info_messages, error_messages)
            else:
                error_messages.append(_("Your modification have not be saved. Some errors were found in the submitted "
                                        "data. Go back to the form you were editing to see what was wrong."))
        elif delete_study_form.delete.data:
            __handle_delete_study_form(delete_study_form, info_messages, error_messages)

        __handle_connect_study_form(connect_study_form, info_messages, error_messages)

    # Get all studies which have been registered
    studies = StudyDAO.get_instance().get_all()
    return render_template('home/index.html',
                           title=_("Home"),
                           new_study_form=new_study_form,
                           delete_study_form=delete_study_form,
                           connect_study_form=connect_study_form,
                           error_messages=error_messages,
                           info_messages=info_messages,
                           studies=studies)
