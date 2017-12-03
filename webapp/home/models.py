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
import datetime

import twunet.tweets
import twunet.users
from twunet.tweets import DatabaseConnection as TweetsDatabaseConnection
from twunet.users import DatabaseConnection as UsersDatabaseConnection
from webapp import db


class UserDB(twunet.users.MySQLDB, db.Model):
    """
    :param id : ID of the entry in the user database
    :type int
    :param host : host of the user database
    :type str
    :param port : port of user database
    :type int
    :param user : name of database
    :type str
    :param password : password of user database
    :type str
    :param database : type of database
    :type str
    :param configuration : foreign key related to id of study name
    :type int
    
    """
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(255))
    port = db.Column(db.Integer)
    user = db.Column(db.String(255))
    password = db.Column(db.String(255))
    database = db.Column(db.String(255))
    configuration = db.Column(db.BigInteger, db.ForeignKey('study.id'))


    def __init__(self, host, port, user, password, database):
        """
        Initialization function : Initialize a User database
        
        :param host: host of the user database
        :type str
        :param port: port used by database
        :type int
        :param user: name of the user
        :type str
        :param password: password set by the user
        :type str
        :param database: database used
        :type str
        """""
        db.Model.__init__(self)
        twunet.users.MySQLDB.__init__(self, host, port, user, password, database)


class TweetsDB(twunet.tweets.MongoDB, db.Model):
    """
        :param id : ID of the entry in the user database
        :type int
        :param host : host of the user database
        :type str
        :param port : port of user database
        :type int
        :param database : type of database
        :type str
        :param configuration : foreign key related to id of study name
        :type int

    """
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(255))
    port = db.Column(db.Integer)
    database = db.Column(db.String(255))
    configuration = db.Column(db.BigInteger, db.ForeignKey('study.id'))

    def __init__(self, host, port, database):
        """
        Initialization function : Initialize a Tweets database
        
        :param host: host address of the tweets database
        :type str
        :param port: port address of the tweets database
         :type int
        :param database: Database used
         :type str 
        """
        db.Model.__init__(self)
        twunet.tweets.MongoDB.__init__(self, host, port, database)


class StudyState(db.Model):
    """
        :param id : ID of the entry in the user database
        :type int
        :param study_id : ID of the study
        :type int
        :param study : Parameter to link this with Study
        :param connected : To check whether connection has been established or not
        :type bool

    """
    __bind_key__ = 'non-persistent-configuration'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    study_id = db.Column(db.Integer, db.ForeignKey('study.id'))
    study = db.relationship('Study', uselist=False)
    connected = db.Column(db.Boolean, default=False)

    def __init__(self, study, connected=False):
        self.study = study
        self.connected = connected

    def setConnected(self):
        self.connected = True

    def setDisconnected(self):
        self.connected = False


class Study(db.Model):
    """
    :param id : ID of study
    :type int
    :param user_db : To establish relationship with user database
    :param tweets_db : To establish relationship with tweets database
    :param name : name of the study
    :type  str
    :param description : Description of the study
    :type str
    :param created_at : Date of creation
    :type datetime
    """
    id = db.Column(db.Integer, primary_key=True)
    user_db = db.relationship("UserDB", uselist=False, cascade="all, delete-orphan")
    tweets_db = db.relationship("TweetsDB", uselist=False, cascade="all, delete-orphan")
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime)

    def __init__(self, name, description, user_db, tweets_db, ):
        """
        # Initialization function: Initialize a study
        
        :param name: Name of the study
        :type str
        :param description: Description of the study
         :type str
        :param user_db: User database which will be used
         :type UserDB instance
        :param tweets_db: Tweets database which will be used
        :type TweetsDB instance
        """
        db.Model.__init__(self)
        self.user_db = user_db
        self.tweets_db = tweets_db
        self.name = name
        self.description = description
        self.created_at = datetime.datetime.now()

    @classmethod
    def from_study_form(cls, study_form):
        """
        # To initialize a new study: Initializes a user database, tweets database
         and a study instance
        
        :param study_form: Form submitted by the user
        :return: An instance of the study
        """
        u = UserDB(host=study_form.user_db_host.data,
                   port=study_form.user_db_port.data,
                   user=study_form.user_db_user.data,
                   password=study_form.user_db_password.data,
                   database=study_form.user_db_name.data)
        t = TweetsDB(host=study_form.tweets_db_host.data,
                     port=study_form.tweets_db_port.data,
                     database=study_form.tweets_db_name.data)
        study = Study(name=study_form.name.data,
                      description=study_form.description.data,
                      user_db=u, tweets_db=t)
        return study



    def update_with_form(self, study_form):
        """
        # To update an existing study: Update details of a study which is 
        already in use
        
        :param study_form: the updated study form
        :return: Updated instance of a study
        """
        self.name = study_form.name.data
        self.description = study_form.description.data

        self.user_db.host = study_form.user_db_host.data
        self.user_db.port = study_form.user_db_port.data
        self.user_db.database = study_form.user_db_name.data
        self.user_db.user = study_form.user_db_user.data
        self.user_db.password = study_form.user_db_password.data

        self.tweets_db.host = study_form.tweets_db_host.data
        self.tweets_db.port = study_form.tweets_db_port.data
        self.tweets_db.database = study_form.tweets_db_name.data


    @property
    def is_connected(self):
        """
        # Check if connection is established

        :return: Boolean value whether the study is connected or not
        """
        return StudyStateDAO.get_instance().is_connected(self)

    def connect(self):
        """
        # Connect a study 
        
        :return: A study instance 
        """
        if not self.is_connected:
            UsersDatabaseConnection.get_instance().init(self.user_db)
            TweetsDatabaseConnection.get_instance().init(self.tweets_db)

            study_state = StudyStateDAO.get_instance().find(self)
            if study_state:
                study_state = StudyStateDAO.get_instance().find(self)
                study_state.setConnected()
                StudyStateDAO.get_instance().update(study_state)
            else:
                StudyStateDAO.get_instance().save(StudyState(self, True))

    def disconnect(self):
        """
        # Disconnect a study
        :return: None
        """
        if self.is_connected:
            UsersDatabaseConnection.get_instance().disconnect()
            TweetsDatabaseConnection.get_instance().disconnect()

            study_state = StudyStateDAO.get_instance().find(self)
            study_state.setDisconnected()
            StudyStateDAO.get_instance().update(study_state)
            print(study_state)


class StudyDAO:
    # Singleton instance
    instance = None

    @classmethod
    def get_instance(cls):
        """

        :rtype: StudyDAO
        """
        if cls.instance is None:
            cls.instance = StudyDAO()
        return cls.instance

    def save(self, study):
        # save a study

        db.session.add(study)
        db.session.commit()


    def update(self, study):
        # Update a study

        db.session.commit()


    def delete(self, study):
        """
        Delete an already existing study
        
        :param study: An instance of study 
        :return:None
        """

        db.session.delete(study)
        db.session.commit()

    def find(self, study_id):
        """
        To find a study by ID
        :param study_id: id of the study to be found
        :return: study instance with the id 'study_id'
        """
        return db.session.query(Study).filter_by(id=study_id).scalar()

    def get_all(self):
        """
        # Get all the registered studies
        
        :return: All study objects in a list 
        """
        return db.session.query(Study).all()

    def get_by_name(self, study_name):
        """
        Find a study by name 
        
        :param study_name: Name of the study to be found
        :return: Instance of the study having the name 'study_name'
        """
        return db.session.query(Study).filter_by(name=study_name).scalar()


class StudyStateDAO:
    # Singleton instance
    instance = None

    @classmethod
    def get_instance(cls):
        """

        :rtype: StudyStateDAO
        """
        if cls.instance is None:
            cls.instance = StudyStateDAO()
        return cls.instance


    def save(self, connected_study):
        # Save a study

        db.session.add(connected_study)
        db.session.commit()

    def update(self, connected_study):
        # Update a study
        db.session.commit()

    def delete(self, connected_study):
        """
        Delete an already existing and connected study

        :param connected_study: An instance of a connected study 
        :return:None
        """
        db.session.delete(connected_study)
        db.session.commit()

    def find(self, connected_study):
        """
        Find a study by its id
        
        :param connected_study: An instance of an already connected study
        :return: An object of type StudyState with the id as connected_study_id
        """
        return db.session.query(StudyState).filter_by(id=connected_study.id).scalar()

    def is_connected(self, study):
        """
        Check if the study is connected or not
        :param study: An instance of Study class
        :return: boolean value true or false
        """
        is_connected = False
        study_state = db.session.query(StudyState).filter_by(study_id=study.id, connected=True).scalar()
        if study_state:
            is_connected = True
        return is_connected

    def get_all(self):
        """
        :return: All connected studies
        """
        return db.session.query(StudyState).all()

    def get_by_name(self, connected_study_name):
        """
        Find a connected study by its name
        
        :param connected_study_name: name of the study required
        :return: A connected study object
        """
        return db.session.query(StudyState).filter_by(name=connected_study_name).scalar()

