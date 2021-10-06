import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_DATABASE_URI = "postgresql://raulb:password@localhost/db_rs"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://flask:password@0.0.0.0:4000/user_roles"
