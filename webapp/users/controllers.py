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
from flask import request, redirect, url_for, make_response, send_file, Response

from webapp.home.models import StudyDAO
from webapp.users.forms import Filter, Exclude, Save, downloadForm
from webapp.users.models import UserDAO
from twunet.tweets import TweetDAO
from webapp.users.models import ExcludedUsers, ExcludedUsersDAO, savedFiltersAndExclusions, savedFiltersAndExclusionsDAO
import math, re
users = Blueprint('users', __name__, url_prefix='/users')
default_breadcrumb_root(users, '.')

filename = "../../web-app/webapp/static/usernames.txt"
usersList = []

def include_user(name , profile):
    """
    Decide whether to include a user or not
    :param name: Name, screen name or location of the user
    :param profile: Profile in which we have to check whether the name exists
    :return: Boolean value true or false
    """
    if ((name in profile.name.lower()) or (name in profile.screen_name.lower())
    or (name in profile.location.lower())):
        return True
    else:
        return False

def get_excluded_users():
    """
    Get all permanent exclusions and add temporary exclusions to the list
    
    :return: IDs of all the permanently excluded users 
    """
    permanentExclusions = ExcludedUsersDAO.get_instance().get_all()
    permanentExcludedIds = []
    for user in permanentExclusions:
        permanentExcludedIds.append(user.user_id)
    return permanentExcludedIds

def saveFiltersAndExclusions(exclude, names, types, save):
    """
    Save the current filters and temporarily excluded users
    
    :param exclude: An object of the Exclude form
    :param names: A list of names to be included or excluded
    :param types: This has the corresponding information of the names whether it has to be included or excluded
    :param save: An object of Save form 
    :return: None
    """
    string_of_names = ','.join(names)
    string_of_types = ','.join(str(type) for type in types)
    exclusions = ','.join(exclude.exclude_temporary)
    savedFiltersAndExclusionsDAO.get_instance().save(savedFiltersAndExclusions.from_users_list
                                                     (save.nameOfSearch.data, save.description.data, string_of_names,
                                                      string_of_types, exclusions))

def exportSavedFilters(name, exclude, filter):
    """
    To reload previously applied filters and exclusions
    :param name: name of the saved filter
    :param exclude: An instance of the exclude form
    :param filter: An instance of the filter form
    :return: 
    """
    savedFilter = savedFiltersAndExclusionsDAO.get_instance().find(name)
    if savedFilter is not None:
        for id in savedFilter.exclusions.split(','):
            exclude.exclude_temporary.append(id)
        wordsToFilter = savedFilter.filterWords.split(',')
        typesOfFilter = savedFilter.filterNumbers.split(',')

        for i in range(0, len(wordsToFilter)):
            if (typesOfFilter[i] == "included"):
                filter.entries.append((wordsToFilter[i], "included"))
            elif(typesOfFilter[i]=="excluded"):
                filter.entries.append((wordsToFilter[i], "excluded"))
    else:
        print("Filter not found")


def get_NamesAndTypesOfFilters(entries):
    """
    Create two lists out of the entries appended in the filter
    
    :param entries: The entries in the filter form 
    :return: Two lists one containing the names and the 
    other the corresponding type included or excluded
    """
    names = [name[0] for name in entries]
    types = [name[1] for name in entries]
    return names, types

def add_permanentExclusions(exclude):
    """
    Adds the users which are permanently excluded in the database
    
    :param exclude: An instance of the exclude form
    :return: None
    """
    for id in exclude.selected_users:
        if id not in exclude.exclude_temporary:
            exclude.exclude_temporary.append(id)
    if exclude.excludePermanent.data:
        for id in exclude.selected_users[-(exclude.present_counts[-1]):]:
            if not (ExcludedUsersDAO.get_instance().find(id)):
                ExcludedUsersDAO.get_instance().save(ExcludedUsers.from_user_id(id))

def add_filters(filter,names):
    """
    To add the filters in the entries list of the Filter form
    
    :param filter: An instance of the Filter form 
    :param names: contains the names to be included or eexcluded
    :return: None
    """
    if filter.register.data and filter.name.data not in names:
        filter.entries.append((filter.name.data, "included"))
    elif filter.unregister.data and filter.name.data not in names:
        filter.entries.append((filter.name.data, "excluded"))

@users.route('/download_tweets/<filename>')
@register_breadcrumb(users, '.users', _('List users'), ('Download tweets'))
def send_download_file(filename):
    global usersList
    ids = []
    for user in usersList:
        ids.append(str(user.tweets)+"\n")
    string_of_ids = ''.join(ids)
    #csv = "vbhjbdss"
    response = make_response(string_of_ids)
    response.headers["Content-Disposition"] = "attachment; filename = twitter_ids.txt"
    return response
    """userTweets = []
    for user in userList:
        tweets = user.tweets
        for tweet in tweets:
            if str(tweet['text']).startswith('RT') or str(tweet).startswith('rt'):
                continue
            else:
                text = re.sub(r"http\S+", "", tweet['text'])
                userTweets = userTweets.append(text+"\n")
                print (text)

    response = make_response(userTweets)

    response.headers["Content-Disposition"] = "attachment; filename=tweets.txt"
    """
    #return send_file('users/usernames.txt', as_attachment=True, attachment_filename=filename)

@users.route('/database/<database_name>/list/<int:page>/<int:number>', methods=['GET','POST'])
@register_breadcrumb(users, '.users', _('List users'))
def users_list(database_name, page, number):
    """
    This function is responsible for all the actions which can be performed
    on the users page
    
    :param database_name: Name of the database
     :type str
    :param page: The page on which we are
     :type int
    :param number: The number of users to be displayed on the page 
    :type int
    :return: Template of users/list.html
    """
    global usersList
    filter = Filter(request.form)
    exclude = Exclude(request.form)
    save = Save(request.form)
    study = StudyDAO.get_instance().get_by_name(database_name)
    download_form = downloadForm(request.form)
    past_filters = savedFiltersAndExclusionsDAO.get_instance().get_all()
    study.connect()
    if len(filter.entries)>0:
        usersList, length = UserDAO.get_instance().get_filtered_users(int(page), int(number), filter.entries)
    else:
        usersList, length = UserDAO.get_instance().get_relevant_users_page_wise(int(page), int(number))

    profiles = []
    list_of_user_ids = []
    for user in usersList:
        list_of_user_ids.append(user.twitter_id_str)
    number_of_pages = math.ceil(float(length) / int(number))
    names, types = get_NamesAndTypesOfFilters(filter.entries)

    if(request.args.get('sData')):  # sData is selected data
        if request.args.get('sData'):
            selected_users = request.args.get('sData')
            selected_list = selected_users.split(',')
            exclude.present_counts.append(len(selected_list))
            for id in selected_list:
                if id not in exclude.selected_users:
                    exclude.selected_users.append(id)

    # If data is submitted
    if request.method=='POST':

        if save.removeAllFilters.data:
            exclude.exclude_temporary=[]
            filter.entries=[]
            exclude.selected_users = []

        if filter.validate():
            add_filters(filter, names)
            names, types = get_NamesAndTypesOfFilters(filter.entries)
            if(len(filter.entries)>0):
                usersList, length = UserDAO.get_instance().get_filtered_users(int(page), int(number), filter.entries)
                number_of_pages = math.ceil(float(length) / int(number))

            else:
                usersList, length = UserDAO.get_instance().get_relevant_users_page_wise(int(page), int(number))
                number_of_pages = math.ceil(float(length)/ int(number))

        if exclude.validate() and exclude.present_counts:
            add_permanentExclusions(exclude)

        if save.saveFilters.data:
            saveFiltersAndExclusions(exclude, names, types, save)

        if save.exportSavedFilters.data:
            print(save.findName.data)
            exportSavedFilters(save.findName.data, exclude, filter)

        if download_form.download.data:
            if download_form.validate():
                send_download_file(download_form.name.data)
                print("Sending data")


    excludedIDs = get_excluded_users()

    for user in usersList:
        if(str(user.current_profile.user_id) not in exclude.exclude_temporary and user.current_profile.user_id not in excludedIDs):
            profiles.append(user.current_profile)

    with open(filename,'w') as f:
        [f.write(str(profile.user_id)+'\n') for profile in profiles]
    f.close()

    return render_template('users/list.html', title=_("List users"), database_name=database_name, users=usersList,
                           profiles=profiles, length=int(number_of_pages), page=int(page), number=int(number),
                           filter= filter, exclude=exclude, save=save, past_filters= past_filters, download_form=download_form)
