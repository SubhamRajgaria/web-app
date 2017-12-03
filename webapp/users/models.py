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

from webapp import db
import twunet
from twunet.users import User, UserProfile, Category
from sqlalchemy import and_, or_, func, not_

class ExcludedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    def __init__(self, user_id):
        db.Model.__init__(self)
        self.user_id = user_id

    @classmethod
    def from_user_id(cls, id):
        exc = ExcludedUsers(id)
        return exc

class UserDAO(twunet.users.UserDAO):
    instance = None

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance

        :return: the instance
        :rtype: UserDAO
        """
        if cls.instance is None:
            cls.instance = UserDAO()
        return cls.instance

    def get_relevant_users_page_wise(self, page=5, number_per_page=10):
        """
        Get users that are considered relevant depending on the page number and number per page
        :param page: which page number we are in
        :param number: how many users per page
        :return: the list of users
        """
        q = self.connection.db.query(User).join(UserProfile).filter(
            Category.relevant.is_(True)
        ).distinct()

        return (q.offset(number_per_page * (page - 1)).limit(number_per_page).all(), q.count())

    def get_filtered_users(self, page=1, number_per_page=10, filters =[('la Rochelle',1)]):
        """
        Get filtered users from the page

        :param page: The page number on which we are
        :param number_per_page: The number of entries per page to be displayed
        :param filter_names: the strings to be excluded opr included
        :param filter_types: to know whether the corresponding string will be included or excluded

        :return: a list of filtered users
        """

        combined_filters = None
        for name, type in filters:
            if type=="included":
                temp_filters =  self.connection.db.query(User).join(UserProfile).filter(
                    and_(Category.relevant.is_(True),or_(func.lower(UserProfile.name).contains(func.lower(name)),
                                                         or_(func.lower(UserProfile.screen_name).contains(func.lower(name)),
                                                             func.lower(UserProfile.location).contains(func.lower(name)))))
                ).distinct()
                if combined_filters is not None:
                    combined_filters = combined_filters.union(temp_filters)
                else:
                    combined_filters = temp_filters

            if type=="excluded":
                temp_filters = self.connection.db.query(User).join(UserProfile).filter(
                    and_(Category.relevant.is_(True), not_(or_(func.lower(UserProfile.name).contains(func.lower(name)),
                                                          or_(func.lower(UserProfile.screen_name).contains(
                                                              func.lower(name)),
                                                              func.lower(UserProfile.location).contains(
                                                                  func.lower(name))))))).distinct()
                if combined_filters is not None:
                    combined_filters = combined_filters.filter(temp_filters.subquery().c.twitter_id_str== UserProfile.user_id)

                else:
                    combined_filters = temp_filters

        return (combined_filters.offset(number_per_page * (page - 1)).limit(number_per_page).all(), combined_filters.count())


class ExcludedUsersDAO:
    instance = None

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance
        
        :return: the instance
        :rtype : ExcludedUsersDAO
        """
        if cls.instance is None:
            cls.instance = ExcludedUsersDAO()
        return cls.instance

    def save(self, exclusion):
        """
        
        :param exclusion: Add the exclusion
        
        :return: None
        """
        db.session.add(exclusion)
        db.session.commit()

    def find(self, id):
        """
        Find an exclusion by id
        
        :param id: ID which has to be searched 
        
        :return: Query object of ExcludedUsers class
        """
        return db.session.query(ExcludedUsers).filter_by(user_id=id).scalar()

    def get_all(self):
        """
        Get all excluded users 
        
        :return: A list containing the ids of all excluded users 
        """
        return db.session.query(ExcludedUsers).all()

class savedFiltersAndExclusions(db.Model):
    """
    A form to save the filters and exclusions
    
    :param id : id of the saved filter
    :param name : name of the search
    :param description : description of the search
    :param filterWords : words to be filtered
    :param filterNumbers : type of the filter excluded or included
     
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    filterWords = db.Column(db.String(10000), nullable=True)
    filterNumbers = db.Column(db.String(5000), nullable=True)
    exclusions = db.Column(db.String(10000), nullable=True)

    def __init__(self, name, description, filterWords, filterTypes, exclusions):
        """
        Initialize an object of savedFiltersAnd Exclusions class
        
        :param name: Name of the search 
        :type str
        :param description: Description of the search
        :type str
        :param filterWords: Words to be filtered separated by a comma
         :type str
        :param filterNumbers: Type of the filter(separated by a comma)
         :type str
        :param exclusions: List of ids to be excluded separated by a comma
        :type str
        
        """
        db.Model.__init__(self)
        self.name = name
        self.description = description
        self.filterWords = filterWords
        self.filterNumbers = filterTypes
        self.exclusions = exclusions

    @classmethod
    def from_users_list(cls, name, description, filterWords, filterNumbers, exclusions):
        """
        Fucntion to create a search  
        :return: an instance of savedFiltersAndExclusions
        
        """
        savedResult = savedFiltersAndExclusions(name, description, filterWords, filterNumbers,exclusions)
        return savedResult

class savedFiltersAndExclusionsDAO:
    instance = None

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance
        
        :return: the instance
        :rtype: savedFiltersAndExclusionsDAO 
        """
        if cls.instance is None:
            cls.instance = savedFiltersAndExclusionsDAO()
        return cls.instance

    def save(self, savedResult):
        """
        Add a saved result to the database
        
        :param savedResult: An instance of savedFiltersAndExclusions
        :return: None
        """
        db.session.add(savedResult)
        db.session.commit()

    def find(self, name):
        """
        Find a saved result by name
        
        :param name: Name to be searched 
         
        :return: An instance of savedFiltersAndExclusions
        """
        return db.session.query(savedFiltersAndExclusions).filter_by(name = name).scalar()

    def get_all(self):
        """
        Find all results of savedFiltersAndExclusions
        
        :return: All saved results 
        """
        return db.session.query(savedFiltersAndExclusions).all()

