from flask import Flask
from marshmallow import Schema, fields, pre_load, validate, ValidationError
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
ma = Marshmallow()
db = SQLAlchemy()

users_roles = db.Table('users_roles',
                       db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                       db.Column('roles_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True))

roles_skills = db.Table('roles_skills',
                        db.Column('roles_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
                        db.Column('skills_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    roles = db.relationship('Role', secondary=users_roles, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    # Columns
    username = db.Column(db.String(50), nullable=False, unique=True)
    def __init__(self, username):
        self.username = username


class UserSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    ## Relationships
    skills = db.relationship('Skills', secondary=roles_skills, lazy='subquery',
                             backref=db.backref('roles', lazy=True))

    # Columns
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
class RoleSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


##SKILLS
class Skills(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    tag = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False)

    def __init__(self, tag, description):
        self.tag = tag
        self.description = description
class SkillSchema(ma.Schema):
    id = fields.Integer()
    tag = fields.String(required=True)
    description = fields.String()